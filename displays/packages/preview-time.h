#pragma once

#include <cstdio>
#include <cstdlib>
#include <ctime>

inline time_t &preview_epoch_storage() {
  static time_t val = 0;
  return val;
}

inline bool &preview_epoch_initialized() {
  static bool initialized = false;
  return initialized;
}

inline void set_preview_time(const char *iso_utc) {
  struct tm tm_val {};
  const char *end = strptime(iso_utc, "%Y-%m-%d %H:%M:%S", &tm_val);
  if (end == nullptr || *end != '\0') {
    std::fprintf(stderr, "FATAL: Invalid preview_time '%s' (expected 'YYYY-MM-DD HH:MM:SS')\n", iso_utc);
    std::abort();
  }
  preview_epoch_storage() = timegm(&tm_val);
  preview_epoch_initialized() = true;
}

extern "C" {
time_t __real_time(time_t *tloc);

// Override ::time() on the host platform so RealTimeClock::now() returns the
// deterministic timestamp configured in YAML.
time_t __wrap_time(time_t *tloc) {
  if (tloc == nullptr && !preview_epoch_initialized()) {
    std::fprintf(stderr, "FATAL: RealTimeClock read ::time(nullptr) before set_preview_time() was initialized\n");
    std::abort();
  }
  time_t val = preview_epoch_storage();
  if (tloc != nullptr) {
    *tloc = val;
  }
  return val;
}
}  // extern "C"
