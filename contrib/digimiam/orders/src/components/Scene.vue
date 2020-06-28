<template>
  <div class="position-relative">
    <video src="@/assets/background.mp4" autoplay loop/>
    <video
      ref="idleVideo"
      class="position-absolute top-left"
      :style="{opacity: idleOpacity}"
      src="@/assets/marmitron_idle.webm" autoplay loop/>
    <img src="@/assets/conveyor.png" class="position-absolute bottom-left">
    <video
      v-for="(animation, animationIndex) in animations" :key="animationIndex"
      :ref="animation.ref"
      class="position-absolute top-left"
      :style="{opacity: animation.opacity}"
      :src="animation.video"/>
  </div>
</template>

<script>
import orderStore from '@/store/orderStore.js'
import progressionStore from '@/store/progressionStore.js'

export default {
  name: "Scene",
  data() {
    return {
      idleOpacity: 1,
      animations: {
        gaufresque: {
          video: require('@/assets/gaufresque_idle.webm'),
          ref: 'animationGaufresque',
          opacity: 0,
          cartDelay: 7000,
          hideImgItemDelay: 1000,
          duration: 8000,
        },
        potjevleesch: {
          video: require('@/assets/potjevleesch_idle.webm'),
          ref: 'animationPotjevleesch',
          opacity: 0,
          cartDelay: 7000,
          hideImgItemDelay: 1000,
          duration: 8000,
        },
        salade_flamande: {
          video: require('@/assets/salade_idle.webm'),
          ref: 'animationSaladeFlamande',
          opacity: 0,
          cartDelay: 7000,
          hideImgItemDelay: 1000,
          duration: 8000,
        },
        cambraisienne: {
          video: require('@/assets/cambraisienne_idle.webm'),
          ref: 'animationCambraisienne',
          opacity: 0,
          cartDelay: 7000,
          hideImgItemDelay: 1000,
          duration: 8000,
        },
        help: {
          video: require('@/assets/marmitron_help_fr.webm'),
          ref: 'animationHelpFr',
          opacity: 0,
          duration: 64000,
        },
      },
    }
  },
  computed: {
    addItemToCartSignal() {
      return orderStore.state.addItemToCartSignal
    },
    itemIdToAdd() {
      return orderStore.state.itemIdToAdd
    },
    items() {
      return orderStore.state.items
    },
    fireHelpAnimation() {
      return progressionStore.state.fireHelpAnimation
    },
    showMarmitron() {
      return progressionStore.state.showMarmitron
    },
  },
  methods: {
    startAnimation(animationId) {
      this.$refs[this.animations[animationId].ref][0].play()

      let this_ = this

      this.$anime.timeline({
        easing: 'linear',
        complete() {
          this_.$refs.idleVideo.pause()
          this_.$refs.idleVideo.currentTime = 0
        },
      })
      .add({
        targets: this,
        idleOpacity: 0,
        duration: 1000,
      })
      .add({
        targets: this.animations[animationId],
        opacity: 1,
        duration: 300,
      }, '-=1000')
    },
    displayItemInCart() {
      orderStore.commit('displayItemInCart', this.itemIdToAdd)
    },
    resumeIdle(animationId) {
      this.$refs.idleVideo.play()

      let this_ = this

      this.$anime.timeline({
        easing: 'linear',
        complete() {
          this_.$refs[this_.animations[animationId].ref][0].currentTime = 0
          this_.$refs[this_.animations[animationId].ref][0].pause()
          orderStore.commit('unlockSelectorScroll')
        }
      })
      .add({
        targets: this,
        idleOpacity: 1,
        duration: 300,
      })
      .add({
        targets: this.animations[animationId],
        opacity: 0,
        duration: 1000,
      }, '-=300')
    },
    pause() {
      this.$refs.idleVideo.pause()
    },
  },
  watch: {
    addItemToCartSignal() {
      setTimeout(orderStore.commit, this.animations[this.itemIdToAdd].hideImgItemDelay, 'setItemOpacity', {itemId: this.itemIdToAdd, opacity: 0})
      setTimeout(this.displayItemInCart, this.animations[this.itemIdToAdd].cartDelay)
      setTimeout(this.resumeIdle, this.animations[this.itemIdToAdd].duration, this.itemIdToAdd)
      this.startAnimation(this.itemIdToAdd)
    },
    fireHelpAnimation() {
      this.startAnimation('help')
      setTimeout(this.resumeIdle, this.animations.help.duration, 'help')
    },
    showMarmitron() {
      let this_ = this
      this.$anime({
        easing: 'linear',
        complete() {
          this_.$refs.idleVideo.pause()
          this_.$refs.idleVideo.currentTime = 0
        },
        targets: this,
        idleOpacity: 0,
        duration: 1000,
      })
    },
  },
  created() {
    setTimeout(this.pause, 1350)
  }
}
</script>

<style scoped>
.top-left {
  top: 0px;
  left: 0px;
}

.bottom-left {
  bottom: 0px;
  left: 0px;
}
</style>