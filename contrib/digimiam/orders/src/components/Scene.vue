<template>
  <div>
    <video src="@/assets/marmitron_interface_h.264_25_50.mp4" mute autoplay loop></video>
    <!--<img src="@/assets/marmitron_interface.png">-->
  </div>
</template>

<script>
export default {
  name: "Scene",
}
</script>

<style scoped>
video {
  display: block; /* Removes a mysterious margin bottom */
}
</style>