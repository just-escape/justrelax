<template>
  <div>
    <video src="@/assets/scene.webm" mute autoplay loop type="video/webm"></video>
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