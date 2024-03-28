# Define parameters
beta <- 2.5  # Infection rate
gamma <- 1.0  # Recovery rate
contact_rate <- 0.5  # Fraction of population each person connects to
I0 <- 5  # Number of people initially infected
N <- 100  # Total population size
maxtime <- 10  # How long to simulate for
npts <- 100  # Number of time points during the simulation
dt <- maxtime / npts  # Timestep length

# Define Person class
Person <- function() {
  .self <- list(
    S = TRUE,  # People start off susceptible
    I = FALSE,
    R = FALSE
  )
  
  .self$infect <- function() {
    .self$S <- FALSE
    .self$I <- TRUE
  }
  
  .self$recover <- function() {
    .self$I <- FALSE
    .self$R <- TRUE
  }
  
  .self$check_infection <- function(other) {
    if (.self$S & other$I & runif(1) < beta / (N * contact_rate) * dt) {
      .self$infect()
    }
  }
  
  .self$check_recovery <- function() {
    if (.self$I & runif(1) < gamma * dt) {
      .self$recover()
    }
  }
  
  .self
}

# Define Sim class
Sim <- function() {
  # Create arrays
  .self <- list(
    x = seq(0, npts - 1),
    S = rep(0, npts),
    I = rep(0, npts),
    R = rep(0, npts),
    
    people <- lapply(1:N, Person)
  )
  .self$time = .self$x * dt
  
  .self$count = function() {
    S <- sum(sapply(.self$people, function(p) p$S))
    I <- sum(sapply(.self$people, function(p) p$I))
    R <- sum(sapply(.self$people, function(p) p$R))
    return(list(S = S, I = I, R = R))
  }
  
  .self$check_infections = function() {
    for (person1 in .self$people) {
      contacts <- sample(1:N, size = floor(N * contact_rate))
      for (contact in contacts) {
        person2 <- .self$people[[contact]]
        person1$check_infection(person2)
      }
    }
  }
  
  .self$check_recoveries = function() {
    for (person in .self$people) {
      person$check_recovery()
    }
  }
  
  .self$run = function() {
    for (t in .self$x[-length(.self$x)]) {
      .self$check_infections()
      .self$check_recoveries()
      
      # Update results
      counts <- .self$count()
      .self$S[t + 1] <- counts$S
      .self$I[t + 1] <- counts$I
      .self$R[t + 1] <- counts$R
    }
    
    cat("Run finished\n")
  }
  
  .self$plot = function() {
    plot(.self$time, .self$S, type = "l", col = "blue", lwd = 2, xlab = "Time", ylab = "Number of people", main = "SIR Model")
    lines(.self$time, .self$I, type = "l", col = "red", lwd = 2)
    lines(.self$time, .self$R, type = "l", col = "green", lwd = 2)
    legend("topleft", legend = c("Susceptible", "Infectious", "Recovered"))
  }

  .self
}

# Run the simulation
sim <- Sim()
sim$run()
sim$plot()