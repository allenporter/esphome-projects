#pragma once

#include <cstdlib>
#include <ctime>
#include <string>

extern "C" {
time_t __real_time(time_t *tloc);

// Override ::time() on the host platform so RealTimeClock::now() is 100%
// deterministic across runs unless PREVIEW_EPOCH is explicitly overridden.
time_t __wrap_time(time_t *tloc) {
  const char *env_epoch = std::getenv("PREVIEW_EPOCH");
  // Default: 2026-10-18 14:00:00 UTC (Sunday, October 18, 2026 02:00 PM)
  time_t val = 1792332000;
  if (env_epoch != nullptr && env_epoch[0] != '\0') {
    val = static_cast<time_t>(std::strtoll(env_epoch, nullptr, 10));
  }
  if (tloc != nullptr) {
    *tloc = val;
  }
  return val;
}
}  // extern "C"

inline std::string preview_env_or(const char *env_name, const char *fallback) {
  const char *val = std::getenv(env_name);
  return (val != nullptr) ? std::string(val) : std::string(fallback);
}
