<template>
  <div>
    {{ this.formattedTime }}
  </div>
</template>

<script>
export default {
  name: 'SessionTimeClock',
  computed: {
    formattedTime() {
      function pad(num) {
        return ("0" + num).slice(-2);
      }

      if (this.sessionTime == 0 && !this.displayZero) {
        return ""
      }

      var minutes = Math.floor(this.sessionTime / 60)
      var secs = Math.round(this.sessionTime % 60)
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
  props: ['sessionTime', 'displayZero']
}
</script>
