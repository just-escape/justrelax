<template>
  <div class="position-relative">
    <video src="@/assets/fond_marmitron.mp4" autoplay mute loop/>
    <video
      ref="idleVideo"
      class="position-absolute top-left"
      :style="{opacity: idleOpacity}"
      src="@/assets/Idle_marmitron_webm.webm" mute autoplay loop/>
    <video
      v-for="(action, actionIndex) in actions" :key="actionIndex"
      :ref="action.ref"
      class="position-absolute top-left"
      :style="{opacity: action.opacity}"
      :src="action.video" mute/>
  </div>
</template>

<script>
import orderStore from '@/store/orderStore.js'

export default {
  name: "Scene",
  data() {
    return {
      idleOpacity: 1,
      actions: {
        gaufresque: {
          video: require('@/assets/gaufresque.mp4'),
          ref: 'actionGaufresque',
          opacity: 0,
          cartDelay: 7000,
          duration: 8000,
        },
        potjevleesch: {
          video: require('@/assets/potlevlesch.mp4'),
          ref: 'actionPotjevleesch',
          opacity: 0,
          cartDelay: 7000,
          duration: 8000,
        },
        salade_flamande: {
          video: require('@/assets/salade.mp4'),
          ref: 'actionSaladeFlamande',
          opacity: 0,
          cartDelay: 7000,
          duration: 8000,
        },
        cambraisienne: {
          video: require('@/assets/cambraisienne.mp4'),
          ref: 'actionCambraisienne',
          opacity: 0,
          cartDelay: 7000,
          duration: 8000,
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
    cartDelay() {
      return this.actions[this.itemIdToAdd].cartDelay
    },
    actionDuration() {
      return this.actions[this.itemIdToAdd].duration
    },
    actionVideo() {
      return this.$refs[this.actions[this.itemIdToAdd].ref][0]
    },
    items() {
      return orderStore.state.items
    },
  },
  methods: {
    startAction() {
      this.actionVideo.play()

      let this_ = this

      this.$anime.timeline({
        easing: 'linear',
      })
      .add({
        targets: this,
        idleOpacity: 0,
        duration: 1000,
      })
      .add({
        targets: this.actions[this.itemIdToAdd],
        opacity: 1,
        duration: 1000,
      }, '-=1000')
      .add({
        duration: 1,
        update() {
          this_.$refs.idleVideo.pause()
          this_.$refs.idleVideo.currentTime = 0
        }
      })
    },
    displayItemInCart() {
      orderStore.commit('displayItemInCart', this.itemIdToAdd)
    },
    resumeIdle() {
      orderStore.commit('unlockSelectorScroll')
      this.$refs.idleVideo.play()

      let this_ = this

      this.$anime.timeline({
        easing: 'linear',
      })
      .add({
        targets: this,
        idleOpacity: 1,
        duration: 1000,
      })
      .add({
        targets: this.actions[this.itemIdToAdd],
        opacity: 0,
        duration: 1000,
      }, '-=1000')
      .add({
        duration: 1,
        update() {
          this_.actionVideo.currentTime = 0
          this_.actionVideo.pause()
        }
      })
    },
  },
  watch: {
    addItemToCartSignal() {
      // 4 * 1000 is an idle loop
      let timeBeforePosition = 0 // (4 - (this.$refs.idleVideo.currentTime % 4)) * 1000
      setTimeout(this.startAction, timeBeforePosition)
      setTimeout(this.displayItemInCart, timeBeforePosition + this.cartDelay)
      setTimeout(this.resumeIdle, timeBeforePosition + this.actionDuration)
    },
  },
}
</script>

<style scoped>
.top-left {
  top: 0px;
  left: 0px;
}
</style>