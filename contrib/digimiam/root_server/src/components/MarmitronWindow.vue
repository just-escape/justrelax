<template>
  <Window :title="$t('INTELLIGENCE CULINAIRE')" class="position-relative oveflow-hidden">
    <video src="@/assets/marmitron_background.mp4" autoplay loop class="position-absolute"/>
    <video
      src="@/assets/marmitron.webm"
      ref="animationIdle"
      :style="{opacity: idleOpacity}"
      autoplay
      loop
      class="position-absolute"/>
    <video
      v-for="(animation, animationIndex) in animations" :key="animationIndex"
      :ref="animation.ref"
      class="position-absolute"
      :style="{opacity: animation.opacity}"
      :src="animation.video"
    />
  </Window>
</template>

<script>
import Window from '@/components/Window.vue'
import businessStore from '@/store/businessStore.js'

export default {
  name: "MarmitronWindow",
  components: {
    Window,
  },
  data() {
    return {
      idleOpacity: 1,
      animations: {
        animation1: {
          video: require('@/assets/marmitron.webm'),
          ref: 'animation1',
          opacity: 0,
          duration: 8000,
        },
        animation2: {
          video: require('@/assets/marmitron.webm'),
          ref: 'animation2',
          opacity: 0,
          duration: 8000,
        },
        animation3: {
          video: require('@/assets/marmitron.webm'),
          ref: 'animation3',
          opacity: 0,
          duration: 8000,
        },
      },
      animationEndTask: null,
    }
  },
  computed: {
    playingAnimation() {
      return businessStore.state.playingMarmitronAnimation
    },
  },
  methods: {
    animationEnd(resumeIdle) {
      businessStore.commit('playMarmitronAnimation', null)

      if (resumeIdle) {
        this.$refs.animationIdle.play()

        this.$anime({
          easing: 'linear',
          targets: this,
          idleOpacity: 1,
          duration: 1000,
        })
      }
    },
  },
  watch: {
    playingAnimation(newValue, oldValue) {
      let this_ = this

      if (this.animations[newValue] !== undefined) {
        this.$refs[this.animations[newValue].ref][0].play()

        // Animation 3 is the final Marmitron animation
        let resumeIdle = newValue !== 'animation3'

        clearTimeout(this.animationEndTask)
        this.animationEndTask = setTimeout(this.animationEnd, this.animations[newValue].duration, resumeIdle)

        this.$anime.timeline({
          easing: 'linear',
        })
        .add({
          targets: this,
          idleOpacity: 0,
          duration: 1000,
        })
        .add({
          targets: this.animations[newValue],
          opacity: 1,
          duration: 1000,
        }, '-=1000')
        .add({
          duration: 1,
          update() {
            this_.$refs.animationIdle[0].pause()
            this_.$refs.animationIdle[0].currentTime = 0
          },
        })
      }

      if (this.animations[oldValue] !== undefined) {
        this.$anime.timeline({
          easing: 'linear',
        })
        .add({
          targets: this.animations[oldValue],
          opacity: 0,
          duration: 1000,
        })
        .add({
          duration: 1,
          update() {
            this_.$refs[this.animations[newValue].ref][0].currentTime = 0
            this_.$refs[this.animations[newValue].ref][0].pause()
          }
        })
      }
    },
  },
}
</script>