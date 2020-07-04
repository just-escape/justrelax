<template>
  <div>
    <div
      @click="reduceAllVideos"
      class="position-absolute opacifier w-100 h-100"
      :style="{opacity: opacifierOpacity, 'z-index': opacifierZIndex}"
    />

    <div
      v-for="(video, videoIndex) in videos" :key="videoIndex"
      class="position-absolute"
      :style="{'z-index': video.zIndex, top: video.top + 'px', left: video.left + 'px'}"
    >
      <div class="position-relative mb-1">
        <video
          :ref="'ad-' + videoIndex"
          :src="video.src" class="glowing-container"
          :poster="video.poster"
          :style="{width: video.width + 'px', height: video.height + 'px'}"
          :controls="video.controls"
          loop
          disablePictureInPicture
          controlslist="nodownload"
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
import businessStore from '@/store/businessStore.js'

export default {
  name: "ExpandableVideos",
  data() {
    return {
      videos: [
        {
          zIndex: 9,
          src: require("@/assets/videos/zephyr_3000.mp4"),
          poster: require("@/assets/img/zephyr_3000.png"),
          initialTop: 624,
          initialLeft: 1576,
          top: 624,
          left: 1576,
          width: 160,
          height: 90,
          controls: false,
          isExpanded: false,
        },
        {
          zIndex: 9,
          src: require("@/assets/videos/zephyr_3000.mp4"),
          poster: require("@/assets/img/zephyr_3000.png"),
          initialTop: 763,
          initialLeft: 1576,
          top: 763,
          left: 1576,
          width: 160,
          height: 90,
          controls: false,
          isExpanded: false,
        },
        {
          zIndex: 9,
          src: require("@/assets/videos/zephyr_3000.mp4"),
          poster: require("@/assets/img/zephyr_3000.png"),
          initialTop: 902,
          initialLeft: 1576,
          top: 902,
          left: 1576,
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
      if (!businessStore.state.success) {
        this.videos[videoIndex].zIndex = 31
        this.videos[videoIndex].controls = true
        this.videos[videoIndex].isExpanded = true
        this.opacifierZIndex = 30

        let this_ = this

        this.$anime.timeline({
          duration: 800,
          easing: 'easeOutQuad',
          complete: function() {
            // Just in case someone toggles expand three times in 1 second.
            if (this_.videos[videoIndex].isExpanded) {
              this_.$refs['ad-' + videoIndex][0].play()
            }
          }
        })
        .add({
          targets: this.videos[videoIndex],
          top: this.videoExpandedTop,
          left: this.videoExpandedLeft,
          width: this.videoExpandedWidth,
          height: this.videoExpandedHeight,
        })
        .add({
          targets: this,
          opacifierOpacity: 0.35,
        }, '-=800')
      }
    },
    reduceVideo(videoIndex) {
      this.opacifierZIndex = -1
      this.videos[videoIndex].controls = false
      this.videos[videoIndex].isExpanded = false
      this.$refs['ad-' + videoIndex][0].pause()

      let this_ = this

      this.$anime.timeline({
        duration: 800,
        easing: 'easeOutQuad',
        complete: function() {
          // Just in case someone toggles expand three times in 1 second.
          // This would result in the video being expanded but behind the opacity filter.
          if (!this_.videos[videoIndex].isExpanded) {
            this_.videos[videoIndex].zIndex = 9
          }
        },
      })
      .add({
        targets: this.videos[videoIndex],
        top: this.videos[videoIndex].initialTop,
        left: this.videos[videoIndex].initialLeft,
        width: this.videoInitialWidth,
        height: this.videoInitialHeight,
      })
      .add({
        targets: this,
        opacifierOpacity: 0,
      }, '-=800')
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
  z-index: 30;
  background: black;
}
</style>