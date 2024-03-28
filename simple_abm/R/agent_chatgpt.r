# Set parameters
beta <- 2.5  # Infection rate
gamma <- 1.0  # Recovery rate
contact_rate <- 0.5  # Fraction of population each person is connected to
I0 <- 5  # Number of people initially infected
N <- 100  # Total population size
maxtime <- 10  # How long to simulate for
npts <- 100  # Number of time points during the simulation
dt <- maxtime / npts  # Timestep length

# Define the Person class
Person <- R6::R6Class("Person",
  public = list(
    S = TRUE,
    I = FALSE,
    R = FALSE,
    infect = function() {
      self$S <- FALSE
      self$I <- TRUE
    },
    recover = function() {
      self$I <- FALSE
      self$R <- TRUE
    },
    check_infection = function(other) {
      if (self$S && other$I && runif(1) < beta / (N * contact_rate) * dt) {
        self$infect()
      }
    },
    check_recovery = function() {
      if (self$I && runif(1) < gamma * dt) {
        self$recover()
      }
    }
  )
)

# Define the Sim class
Sim <- R6::R6Class("Sim",
  public = list(
    new = function() {
      self$x <- seq(0, maxtime, length.out = npts)
      self$S <- rep(0, npts)
      self$I <- rep(0, npts)
      self$R <- rep(0, npts)
      self$time <- self$x
      self$S[1] <- N - I0
      self$I[1] <- I0
      self$people <- replicate(N, Person$new(), simplify = FALSE)
      invisible(self)
    },
    count = function() {
      S <- sum(sapply(self$people, function(person) person$S))
      I <- sum(sapply(self$people, function(person) person$I))
      R <- sum(sapply(self$people, function(person) person$R))
      return(list(S = S, I = I, R = R))
    },
    check_infections = function() {
      for (person1 in self$people) {
        contacts <- sample(1:N, size = as.integer(N * contact_rate))
        for (contact in contacts) {
          person2 <- self$people[[contact]]
          person1$check_infection(person2)
        }
      }
    },
    check_recoveries = function() {
      for (person in self$people) {
        person$check_recovery()
      }
    },
    run = function() {
      for (t in seq_along(self$x)[-length(self$x)]) {
        self$check_infections()
        self$check_recoveries()
        counts <- self$count()
        self$S[t + 1] <- counts$S
        self$I[t + 1] <- counts$I
        self$R[t + 1] <- counts$R
      }
      print("Run finished")
    },
    plot = function() {
      lines(self$time, self$S, type = "l", col = "blue", xlab = "Time", ylab = "Number of people", main = "SIR Model")
      lines(self$time, self$I, col = "red")
      lines(self$time, self$R, col = "green")
      legend("topright", legend = c("Susceptible", "Infectious", "Recovered"), col = c("blue", "red", "green"), lty = 1)
    }
  )
)

# Run the simulation
sim <- Sim$new()
sim$run()
sim$plot()