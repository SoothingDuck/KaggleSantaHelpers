is_sanctioned_time <- function(tps.minute) {
  return(((tps.minute - (9*60)) %% (24*60)) < (10 * 60))
} 

get.sanctioned.breakdown <- function(start.minute, toy.duration, productivity) {
  toy.required.minutes <- as.integer(ceiling(toy.duration/productivity))
  full_days = as.integer(toy.required.minutes / (24*60)) 
  sanctioned = full_days * 10 * 60
  unsanctioned = full_days * (24 - 10) * 60
  remainder_start = start.minute + (full_days * 24 * 60)
  
  t <- seq(remainder_start, start.minute+toy.required.minutes-1)
  t <- sapply(t, is_sanctioned_time)
  
  sanctioned <- sanctioned + sum(t)
  unsanctioned <- unsanctioned + sum(! t)
  
  return(list(sanctioned=sanctioned, unsanctioned=unsanctioned))
}

get.next.productivity <- function(start.minute, toy.duration, productivity) {
  t <- get.sanctioned.breakdown(start.minute, toy.duration, productivity)
  
  sanctioned <- t$sanctioned
  unsanctioned <- t$unsanctioned
  
  next.p <- max(0.25,
                    min(4.0, productivity * (1.02 ** (sanctioned/60.0)) *
                          (0.9 ** (unsanctioned/60.0))))
  
  return(next.p)
}

next_sanctioned_minute <- function(tps.minute) {
  # next minute is a sanctioned minute
  if(is_sanctioned_time(tps.minute) & is_sanctioned_time(tps.minute+1)) {
    return(tps.minute + 1)
  }
  num_days <- as.integer(tps.minute / (24*60))
  return((9*60) + (num_days + 1) * (24*60))
}

apply_resting_period <- function(start, num_unsanctioned) {
  num_days_since_jan1 <- as.integer(start/(24*60))
  rest_time <- num_unsanctioned
  rest_time_in_working_days <- as.integer(rest_time / (60 * 10))
  rest_time_remaining_minutes <- as.integer(rest_time %% (60 * 10))
  
  local_start <- start %% (24*60)
  
  if(local_start < (9*60)) {
    local_start <- 9*60
  } else {
    if(local_start > ((9+10)*60)) {
      num_days_since_jan1 <- num_days_since_jan1 + 1
      local_start <- 9*60
    }
  }
  
  if(local_start + rest_time_remaining_minutes > ((9+10)*60)) {
    rest_time_in_working_days <- rest_time_in_working_days + 1
    rest_time_remaining_minutes <- rest_time_remaining_minutes - (((9+10)*60))
    local_start <- (9*60)
  }
  
  total_days <- num_days_since_jan1 + rest_time_in_working_days
  
  return((total_days*24*60)+local_start+rest_time_remaining_minutes)
}

# num_days_since_jan1 = start / self.minutes_in_24h
# rest_time = num_unsanctioned
# rest_time_in_working_days = rest_time / (60 * self.hours_per_day)
# rest_time_remaining_minutes = rest_time % (60 * self.hours_per_day)
# 
# # rest time is only applied to sanctioned work hours. If local_start is at an unsanctioned time,
# # need to set it to be the next start of day
# local_start = start % self.minutes_in_24h  # minute of the day (relative to a current day) the work starts
# if local_start < self.day_start:
#   local_start = self.day_start
# elif local_start > self.day_end:
#   num_days_since_jan1 += 1
# local_start = self.day_start
# 
# if local_start + rest_time_remaining_minutes > self.day_end:
#   rest_time_in_working_days += 1
# rest_time_remaining_minutes -= (self.day_end - local_start)
# local_start = self.day_start
# 
# total_days = num_days_since_jan1 + rest_time_in_working_days
# return total_days * self.minutes_in_24h + local_start + rest_time_remaining_minutes
# 

get.next.available.time <- function(start.minute, toy.duration, productivity) {
  toy.required.minutes <- as.integer(ceiling(toy.duration/productivity))
  
  t <- get.sanctioned.breakdown(start.minute, toy.duration, productivity)
  sanctioned <- t$sanctioned
  unsanctioned <- t$unsanctioned
  
  end.minute <- start.minute + toy.required.minutes
  
  if(unsanctioned == 0) {
    if(is_sanctioned_time(end.minute)) {
      return(end.minute)
    } else {
      return(next_sanctioned_minute(end.minute))
    }
  } else {
    return(apply_resting_period(end.minute, unsanctioned))
  }
}

# # Mise à jour next available time
# start_available_working_time = self.get_next_available_working_time()
# start_minute = int(((start_available_working_time-self.__time_base).total_seconds())/60)
# toy_duration = toy.get_duration()
# toy_required_minutes = int(math.ceil(toy_duration / self.rating))
# 
# sanctioned, unsanctioned = self.hrs.get_sanctioned_breakdown(start_minute, toy_required_minutes)
# 
# # enforce resting time based on the end_minute and the unsanctioned minutes that
# # need to be accounted for.
# end_minute = start_minute + toy_required_minutes
# # print(start_minute, end_minute)
# if unsanctioned == 0:
#   if self.hrs.is_sanctioned_time(end_minute):
#   #self.next_available_time = end_minute
#   self.set_next_available_working_time(start_available_working_time+datetime.timedelta(minutes=end_minute-start_minute))
# else:
#   #self.next_available_time = self.hrs.next_sanctioned_minute(end_minute)
#   self.set_next_available_working_time(start_available_working_time+datetime.timedelta(minutes=self.hrs.next_sanctioned_minute(end_minute)-start_minute))
# else:
#   #self.next_available_time = self.hrs.apply_resting_period(end_minute, unsanctioned)
#   self.set_next_available_working_time(start_available_working_time+datetime.timedelta(minutes=self.hrs.apply_resting_period(end_minute, unsanctioned)-start_minute))
# 
# # Mise à jour productivité
# self.rating = max(0.25,
#                   min(4.0, self.rating * (self.rating_increase ** (sanctioned/60.0)) *
#                         (self.rating_decrease ** (unsanctioned/60.0))))
# 

get.productivity.without.unsanctioned <- function(start.productivity, duration) {
  # self.rating = max(0.25,
  #                   min(4.0, self.rating * (self.rating_increase ** (sanctioned/60.0)) *
  #                         (self.rating_decrease ** (unsanctioned/60.0))))
  p <- max(0.25,
           min(4.0,
               start.productivity * (1.02 ** (duration/60.0))
             ))  
  
  return(p)
}

get.next.without.unsanctionned <- function(start, duration) {
  num.days <- as.integer(duration/(10*60))
  remaining.minutes <- duration %% (10*60)
  
  end <- start + (1440*num.days) + remaining.minutes
  
  return(end)
}

