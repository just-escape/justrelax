<template>
  <div>
    <div
      @click="reduceAllVideos"
      class="position-absolute opacifier w-100 h-100"
      :style="{opacity: opacifierOpacity, 'z-index': opacifierZIndex}"
    />

    <div
      v-for="(video, videoIndex) in videos" :key="videoIndex"
      class="position-absolute transition-1s"
      :style="{'z-index': video.zIndex, top: video.top + 'px', left: video.left + 'px'}"
    >
      <div class="position-relative mb-1">
        <video
          :src="video.src" class="glowing-container transition-1s"
          :style="{width: video.width + 'px', height: video.height + 'px'}"
          :controls="video.controls"
        />
        <b-btn v-if="!video.isExpanded" @click="expandVideo(videoIndex)" class="position-absolute lh-1 bottom-right" size="sm" variant="outline-info">
          <i class="text-teal fas fa-expand"/>
        </b-btn>
        <b-btn v-if="video.isExpanded" @click="reduceVideo(videoIndex)" class="position-absolute lh-1 upper-top-right" size="sm" variant="outline-info">
          <i class="text-teal fas fa-times"/>
        </b-btn>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ExpandableVideos",
  data() {
    return {
      videos: [
        {
          zIndex: 9,
          src: require("@/assets/Wireframe.mp4"),
          initialTop: 624,
          initialLeft: 1564,
          top: 624,
          left: 1564,
          width: 160,
          height: 90,
          controls: false,
          isExpanded: false,
        },
        {
          zIndex: 9,
          src: require("@/assets/Wireframe.mp4"),
          initialTop: 763,
          initialLeft: 1564,
          top: 763,
          left: 1564,
          width: 160,
          height: 90,
          controls: false,
          isExpanded: false,
        },
        {
          zIndex: 9,
          src: require("@/assets/Wireframe.mp4"),
          initialTop: 902,
          initialLeft: 1564,
          top: 902,
          left: 1564,
          width: 160,
          height: 90,
          controls: false,
          isExpanded: false,
        },
      ],
      videoInitialWidth: 160,
      videoInitialHeight: 90,
      videoExpandedWidth: 1600,
      videoExpandedHeight: 900,
      videoExpandedTop: 70,
      videoExpandedLeft: 200,
      opacifierZIndex: -1,
      opacifierOpacity: 0,
    }
  },
  methods: {
    expandVideo(videoIndex) {
      this.videos[videoIndex].zIndex = 11
      this.videos[videoIndex].top = this.videoExpandedTop
      this.videos[videoIndex].left = this.videoExpandedLeft
      this.videos[videoIndex].width = this.videoExpandedWidth
      this.videos[videoIndex].height = this.videoExpandedHeight
      this.videos[videoIndex].controls = true
      this.videos[videoIndex].isExpanded = true

      this.opacifierZIndex = 10
      setTimeout(this.setOpacifierOpacity, 1)
    },
    setOpacifierOpacity() {
      this.opacifierOpacity = 0.35
    },
    reduceVideo(videoIndex) {
      this.opacifierZIndex = -1
      this.opacifierOpacity = 0

      this.videos[videoIndex].zIndex = 9
      this.videos[videoIndex].top = this.videos[videoIndex].initialTop
      this.videos[videoIndex].left = this.videos[videoIndex].initialLeft
      this.videos[videoIndex].width = this.videoInitialWidth
      this.videos[videoIndex].height = this.videoInitialHeight
      this.videos[videoIndex].controls = false
      this.videos[videoIndex].isExpanded = false
    },
    reduceAllVideos() {
      for (var i = 0 ; i < this.videos.length ; i++) {
        this.reduceVideo(i)
      }
    },
  },
}
</script>

<style scoped>
.opacifier {
  top: 0px;
  left: 0px;
  z-index: 10;
  background: black;
  transition: opacity 1s;
}

.transition-1s {
  transition: all 1s;
}

video:focus {
  outline: none !important;
}
</style>