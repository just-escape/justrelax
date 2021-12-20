<template>
  <div>
    {{ formattedTime }}
  </div>
</template>

<script>
export default {
  name: 'Clock',
  computed: {
    formattedTime() {
      function pad(num) {
        return ("0" + num).slice(-2);
      }

      if (this.seconds === undefined || this.seconds === null) {
        return ""
      }

      if (this.seconds == 0 && !this.displayZero) {
        return ""
      }

      var minutes = Math.floor(this.seconds / 60)
      var secs = Math.round(this.seconds % 60)
      var hours = Math.floor(minutes / 60)
      minutes = minutes % 60
      var time = pad(minutes) + ":" + pad(secs)

      if (hours > 9)
      {
        time = ">10h"
      } else if (hours > 0) {
        time = hours + ":" + time
      }

      return time
    }
  },
  props: ["seconds", 'displayZero']
}
</script>
