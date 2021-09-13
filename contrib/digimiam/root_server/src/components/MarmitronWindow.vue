<template>
  <Window :title="$t('cooking_ai')" class="position-relative oveflow-hidden">
    <video src="@/assets/videos/server_background_862x670.mp4" autoplay loop class="position-absolute"/>
    <video
      src="@/assets/videos/marmitron_idle_loop_862x670.webm"
      ref="animationIdle"
      :style="{opacity: idleOpacity}"
      autoplay
      loop
      class="position-absolute"/>
    <div v-for="(animation, animationIndex) in animations" :key="animationIndex">
      <video
        v-for="(localizedAnimation, lang) in animation" :key="animationIndex + lang"
        :ref="localizedAnimation.ref"
        class="position-absolute"
        :style="{opacity: localizedAnimation.opacity}"
        :src="localizedAnimation.video"
      />
    </div>
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
      // Is updated only when a video is not playing
      videoLang: this.$i18n.locale,
      idleOpacity: 1,
      animations: {
        reponse: {
          en: {
            video: require('@/assets/videos/marmitron_password_en_862x670.webm'),
            ref: 'reponseEn',
            opacity: 0,
            duration: 23960,
          },
          fr: {
            video: require('@/assets/videos/marmitron_password_fr_862x670.webm'),
            ref: 'reponseFr',
            opacity: 0,
            duration: 23960,
          },
        },
        liberation: {
          en: {
            video: require('@/assets/videos/marmitron_liberation_en_862x670.webm'),
            ref: 'liberationEn',
            opacity: 0,
            duration: 8000,
          },
          fr: {
            video: require('@/assets/videos/marmitron_liberation_fr_862x670.webm'),
            ref: 'liberationFr',
            opacity: 0,
            duration: 8000,
          },
        },
        beer: {
          en: {
            video: require('@/assets/videos/marmitron_beer_862x670.webm'),
            ref: 'beerEn',
            opacity: 0,
            duration: 16000,
          },
          fr: {
            video: require('@/assets/videos/marmitron_beer_862x670.webm'),
            ref: 'beerFr',
            opacity: 0,
            duration: 16000,
          },
        },
      },
      animationEndTask: null,
    }
  },
  computed: {
    playingAnimation() {
      return businessStore.state.playingMarmitronAnimation
    },
    locale() {
      return this.$i18n.locale
    },
  },
  methods: {
    animationEnd(resumeIdle) {
      businessStore.commit('playAnimation', null)

      if (resumeIdle) {
        this.$refs.animationIdle.play()

        this.$anime({
          easing: 'linear',
          targets: this,
          idleOpacity: 1,
          duration: 300,
        })
      }
    },
  },
  watch: {
    locale(newValue) {
      if (!this.animationEndTask) {
        // Otherwise, wait for the end of the animation to update
        this.videoLang = newValue
      }
    },
    playingAnimation(newValue, oldValue) {
      let this_ = this

      if (newValue !== null) {
        this.$refs[this.animations[newValue][this.videoLang].ref][0].play()

        // liberation is the final Marmitron animation
        let resumeIdle = newValue !== 'liberation'

        clearTimeout(this.animationEndTask)
        this.animationEndTask = setTimeout(this.animationEnd, this.animations[newValue][this.videoLang].duration, resumeIdle)

        this.$anime.timeline({
          easing: 'linear',
          complete() {
            this_.$refs.animationIdle.pause()
            this_.$refs.animationIdle.currentTime = 0
          },
        })
        .add({
          targets: this,
          idleOpacity: 0,
          duration: 1000,
        })
        .add({
          targets: this.animations[newValue][this.videoLang],
          opacity: 1,
          duration: 300,
        }, '-=1000')
      }

      if (oldValue !== null) {
        this.$anime.timeline({
          easing: 'linear',
          complete() {
            this_.$refs[this_.animations[oldValue][this_.videoLang].ref][0].currentTime = 0
            this_.$refs[this_.animations[oldValue][this_.videoLang].ref][0].pause()
            this_.videoLang = this_.locale
          },
        })
        .add({
          targets: this.animations[oldValue][this.videoLang],
          opacity: 0,
          duration: 1000,
        })
      }
    },
  },
}
</script>