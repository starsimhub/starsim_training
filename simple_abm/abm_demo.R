######################################## 
# Robyn Stuart
# April 2024
######################################## 


######################################## 
# Agent based model
# Structure: SEIR (sus, exposed, infected, recovered)
# Agents are defined by their properties:
#   * person number
#   * disease state
#   * propensity for mixing (how much they are likely to mix with other agents)
# Population:
#   * a collection of agents
# Interactions:
#   * we will build these up over time, but initially the rules are S+E => E+E
######################################## 
# Define a population with 1 exposed person
Population <- data.frame(AgentNo = 1,
                         State = "E", 
                         Mixing = runif(1,0,1)) # Draw a random number that determines how much they like to mix

# Now add 9 susceptible people to the population
nPop <- 10
for (i in 2:nPop){
  Agent <- data.frame(AgentNo = i,
                       State = "S",
                       Mixing = runif(1,0,1))
  Population <- rbind(Population, Agent)
}

# Let's look at the agents
View(Population)

# Notice a couple of things: 
#     - if we run it again, the mixing numbers change
#     - we've defined their properties, now we need to know how interactions change these.


# Now we need to move them through time
# Let's look at Agent 1 in the model

# First we pull out their propensity of mixing/socialising
Mix1 <- Population$Mixing[1]

# Then we use this to determine how many people they'll meet
Contacts1 <- round(Mix1*3, 0) # Here we assume they meet 0-3 people

# Then we figure out who these people they meet are
ContactNos1 <- sample(1:nPop, Contacts1, replace=TRUE)
# This tells us that person 1 meets "Contact1" people, and we also know who these people are
# Now let's see what happens at each of these meetings!

# Loop over all of this person's contacts
for (j in 1:length(ContactNos1)) {
  # Grab who they meet
  Agent <- Population[ContactNos1[j],]
  # If they meet someone who's exposed, then they become exposed
  if (Agent$State=="E"){
    Population$State[1] <- "E"
  }
}

#######
# We need to do this for everyone in the model: let's make another loop.
for (i in 1:nPop) {
  # First we pull out this person's propensity of mixing/socialising
  Mix <- Population$Mixing[i]
  # Then we use this to determine how many people they'll meet
  Contacts <- round(Mix*3,0)
  # Then we figure out who these people they meet are
  ContactNos <- sample(1:nPop, Contacts, replace=TRUE)
  # Did they meet anyone?
  if (length(ContactNos)>0){ 
    # Now let's see what happens at each of these meetings!
    for (j in 1:length(ContactNos)) {
      # Grab who they meet
      Agent <- Population[ContactNos[j],]
      # If they meet someone who's exposed, then they become exposed
      if (Agent$State=="E"){
        Population$State[i] <- "E"
      }
    }
  }
}

# Let's look at the population again
View(Population)

# Lots of people have become exposed! 
# Eventually, everyone is exposed
# An easier way to see this is to look at a summary table.
table(Population$State) 
# This means we can simulate more people and just look at the summary statistics

# Let's make it a little more realistic. We'll remake the population and
# take the same code as we used above, but now we'll incorporate the info
# about how likely people are to mix
Population <- data.frame(AgentNo = 1,
                         State = "E",
                         Mixing = runif(1,0,1))
nPop1 <- 100
for (i in 2:nPop1){
  Agent <- data.frame(AgentNo = i,
                      State = "S",
                      Mixing = runif(1,0,1))
  Population <- rbind(Population, Agent)
}

# Now we'll simulate what happens over a single timestep
for (i in 1:nPop1) {
  # First we pull out this person's propensity of socialising
  Mix <- Population$Mixing[i]
  # Then we use this to determine how many people they'll meet
  Contacts <- round(Mix*3,0) + 1 # CHANGE 1: ensure that everyone meets at least 1 person
  # Then we figure out who these people they meet are
  ContactNos <- sample(1:nPop1,
                       Contacts, 
                       replace=TRUE,
                       prob=Population$Mixing) # CHANGE 2: Use mixing probabailities
  # Now let's see what happens at each of these meetings!
  for (j in 1:length(ContactNos)) {
    # Grab who they meet
    Agent <- Population[ContactNos[j],]
    if (Agent$State=="E"){
      # CHANGE 3: Toss a coin to figure out if they get exposed at this meeting
      Coin <- runif(1,0,1)
      if (Coin < 0.5){
        Population$State[i] <- "E"
      }
    }
  }
}
table(Population$State) 

# After a few steps, nearly everyone is exposed! Let's look at the remaining susceptibles
Population[Population$State=="S",]
# Often, it's people with low mixing parameters that avoid exposure



#################################################
# Simulating the agent-based model over time
#################################################

# Here we define a function that generates our population
PopGen <- function( nPop, E0, I0 ){
  # Inputs:
  # * nPop: population size
  # * E0: number of people initially exposed
  # * I0: number of people initially infected
  # Create a population of susceptibles
  Population <- data.frame( AgentNo = 1:nPop,
                        State = "S",
                        Mixing = runif(nPop,0,1),
                        TimeE = 0, # the time that they remain exposed
                        TimeI = 0, # the duration of their infection
                        stringsAsFactors = FALSE )
  Population$State[1:E0] <- "E"
  Population$TimeE[1:E0] <- rbinom( E0, 13, 0.5) + 1
  Population$State[(E0+1):(E0 + I0)] <- "I"
  Population$TimeI[(E0+1):(E0 + I0)] <- rbinom( I0, 12, 0.5 ) + 1
  return( Population )
}

nPop <- 100
myPop <- PopGen( nPop, E0 = 2, I0 = 3 )

# Generate some parameters
par <- data.frame( MaxMix = 10, # Maximum number of contacts in a day
                    S2E = 0.25, # analagous to beta - the probability of becoming exposed if susceptible
                    E2I = 0.1, 
                    I2D = 0.05) # adding in mortality - each infected person can die

# Now we define a function that simulates our ABM!
ABM <- function( Population, par, nTime ){
  nPop <- nrow( Population )
  Out <- data.frame( S = rep( 0, nTime ),
                      E = rep( 0, nTime),
                      I = rep( 0, nTime),
                      R = rep( 0, nTime),
                      D = rep( 0, nTime))
  # Move the people through time.
  for(k in 1:nTime){  
    # Moving People Through time.
    StateS1 <- (1:nPop)[Population$State == "S" ]
    StateSE1 <- (1:nPop)[Population$State == "S" | 
                           Population$State == "E" ]
    for( i in StateS1 ){
      # Determine if they like to meet others
      Mix <- Population$Mixing[ i ]
      # How many agents will they meet
      Contacts <- round( Mix*par$MaxMix, 0 ) + 1
      # Grab the agents they will meet
      ContactNos <- sample( StateSE1, 
                       Contacts, 
                       replace = TRUE,
                       prob = Population$Mixing[StateSE1] )
      for( j in 1:length(ContactNos) ){
        # Grab who they will meet
        Agent <- Population[ ContactNos[j], ]
        # If exposed change State
        if( Agent$State == "E" ){
          Coin <- runif(1,0,1)
          if( Coin < par$S2E ){
            Population$State[i] <- "E"
          }
        }
      }
    }
    # Grab those who have been exposed and increment time
    StateE1 <- (1:nPop)[Population$State == "E" ]
    Population$TimeE[StateE1] = Population$TimeE[StateE1] + 1
    StateE2 <- (1:nPop)[Population$State == "E" & 
                          Population$TimeE > 14]
    Population$State[ StateE2 ] <- "R"
    # Grab those who could become sick
    StateE3 <- (1:nPop)[Population$State == "E" & 
                          Population$TimeE > 3 ]
    for( i in StateE3 ){
      # Randomly assign whether they get sick or not.
      Coin <- runif(1,0,1)
      if( Coin < par$E2I ){
        Population$State[i] <- "I"
      }
    }
    # Update how long they have been sick.
    StateI1 <- (1:nPop)[Population$State == "I" ]
    Population$TimeI[StateI1] = Population$TimeI[StateI1] + 1
    StateI2 <- (1:nPop)[Population$State == "I" & 
                           Population$TimeI > 14]
    Population$State[ StateI2 ] <- "R"
    StateI3 <- (1:nPop)[Population$State == "I" & 
                           Population$TimeI < 15]
    Population$State[StateI3] <- ifelse( 
      runif( length(StateI3),0,1) > par$I2D, "I", "D")
    
    Out$S[k] <- length( Population$State[Population$State == "S"] )
    Out$E[k] <- length( Population$State[Population$State == "E"] ) 
    Out$I[k] <- length( Population$State[Population$State == "I"] )
    Out$R[k] <- length( Population$State[Population$State == "R"] )
    Out$D[k] <- length( Population$State[Population$State == "D"] ) 
  }
  return( Out )
}

Population <- PopGen( 1000, E0 = 5, I0 = 2 )
par <- data.frame( MaxMix = 5,
                    S2E = 0.15,
                    E2I = 0.1,
                    I2D = 0.01)
Model1 <- ABM( Population, par, nTime = 25 )

# Plot results
library(ggplot2)
library(reshape2)
Model1$t <- seq(1,25)
output_long <- melt(Model1, id = "t") 
ggplot(data = output_long,                                               
       aes(x = t, y = value, colour = variable, group = variable)) +  
  geom_line() +                                                          
  xlab("Time (days)")+                                                   
  ylab("Number of people") +                                
  labs(colour = "Compartment")




