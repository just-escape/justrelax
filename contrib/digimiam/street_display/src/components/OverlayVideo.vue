<template>
  <div class="h-100">
    <video
      src="@/assets/hologram.mp4"
      mute autoplay loop
    ></video>
  </div>
</template>

<script>
export default {
  name: "OverlayVideo",
}
</script>

<style scoped>
video {
  display: block; /* Removes a mysterious margin bottom */
}
</style>
