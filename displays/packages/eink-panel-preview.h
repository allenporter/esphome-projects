#pragma once

#include <ctime>

inline time_t &preview_epoch_storage() {
  static time_t val = 1792332000;  // Default: 2026-10-18 14:00:00 UTC
  return val;
}

inline void set_preview_time(const char *iso_utc) {
  struct tm tm_val {};
  if (strptime(iso_utc, "%Y-%m-%d %H:%M:%S", &tm_val) != nullptr) {
    preview_epoch_storage() = timegm(&tm_val);
  }
}

extern "C" {
time_t __real_time(time_t *tloc);

// Override ::time() on the host platform so RealTimeClock::now() returns the
// deterministic timestamp configured in YAML.
time_t __wrap_time(time_t *tloc) {
  time_t val = preview_epoch_storage();
  if (tloc != nullptr) {
    *tloc = val;
  }
  return val;
}
}  // extern "C"
