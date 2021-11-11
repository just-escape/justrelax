<template>
  <div
    class="password-window z-index-20 position-absolute"
    :style="{top: top, left: left, transform: transform}"
  >
    <Window :title="$t('fallback_authentication')" theme="warning">
      <div class="d-flex flex-column justify-content-between px-3 py-4 h-100 bg-black-transparent text-orange-light">
        <div>
          <div>
            {{ $t('fallback_authentication_is_enabled') }}
          </div>
        </div>
        <div class="d-flex flex-column">
          <div class="font-italic mb-2 text-18">{{ $t('what_is_the_secret_ingredient') }}</div>
          <div
            class="text-18 input-warning p-1 rounded"
          >
            <span v-html="secretAnswer"/>
            <span
              v-if="recordKeyPresses"
              :style="{
                opacity: fullBlockOpacity,
              }"
            >&#9608;</span>
          </div>
        </div>
        <div class="d-flex flex-row justify-content-between">
          <div class="text-red align-self-center" :style="{opacity: errorMessageOpacity}">
            {{ $t('that_is_not_the_right_answer') }}
          </div>
          <div>
            <ButtonOrange class="mr-4" @click="validate">
              {{ $t('confirm') }}
            </ButtonOrange>
            <!-- display: none because some players tend not to pay attention to that window -->
            <ButtonOrange class="d-none" @click="hidePasswordRecoveryWindow">
              {{ $t('cancel') }}
            </ButtonOrange>
          </div>
        </div>
      </div>
    </Window>
  </div>
</template>

<script>
import Window from '@/components/Window.vue'
import ButtonOrange from '@/components/ButtonOrange.vue'
import businessStore from '@/store/businessStore.js'

export default {
  name: "PasswordRecoveryWindow",
  components: {
    Window,
    ButtonOrange,
  },
  data() {
    return {
      topOffset: 350,
      leftOffset: 400,
      scaleX: 0,
      scaleY: 0,
      secretAnswer: '',
      fullBlockOpacity: 1,
      errorMessageOpacity: 0,
      errorMessageOpacityAnimation: this.$anime({}),
    }
  },
  computed: {
    displayed() {
      return businessStore.state.displayPasswordRecoveryWindow
    },
    top() {
      return "calc(0px + " + this.topOffset + "px)"
    },
    left() {
      return "calc(0px + " + this.leftOffset + "px)"
    },
    transform() {
      return "scaleX(" + this.scaleX + ") scaleY(" + this.scaleY + ")"
    },
    lastPressedCharacter() {
      return businessStore.state.lastPressedCharacter
    },
    pressSignal() {
      return businessStore.state.pressSignal
    },
    backspaceSignal() {
      return businessStore.state.backspaceSignal
    },
    crSignal() {
      return businessStore.state.crSignal
    },
    recordKeyPresses() {
      return businessStore.state.displayPasswordRecoveryWindow
    },
  },
  methods: {
    validate() {
      if (businessStore.state.secretAnswers.includes(this.secretAnswer)) {
        this.errorMessageOpacityAnimation.pause()
        this.errorMessageOpacityAnimation = this.$anime({
          targets: this,
          errorMessageOpacity: 0,
          duration: 500,
          easing: 'easeInQuad',
        })
        businessStore.commit('success')
      } else {
        this.errorMessageOpacityAnimation.pause()
        this.errorMessageOpacity = 1
        this.errorMessageOpacityAnimation = this.$anime({
          targets: this,
          errorMessageOpacity: 0,
          duration: 7000,
          easing: 'easeInQuad',
        })
        this.secretAnswer = ''
      }
      businessStore.commit('passwordRecoveryTry', this.secretAnswer)
    },
    hidePasswordRecoveryWindow() {
      businessStore.commit('hidePasswordRecoveryWindow')
    },
  },
  watch: {
    displayed(newValue) {
      if (newValue) {
        this.$anime.timeline({
          targets: this,
        })
        .add({
          scaleX: 1,
          scaleY: 1,
          duration: 400,
          easing: 'easeInQuad',
        })
        .add({
          leftOffset: 110,
          topOffset: 340,
          duration: 700,
          easing: 'easeOutQuad',
        }, '-=700')
      } else {
        this.$anime.timeline({
          targets: this,
        })
        .add({
          scaleX: 0,
          scaleY: 0,
          duration: 700,
          easing: 'easeInOutQuad',
        })
        .add({
          leftOffset: 400,
          topOffset: 350,
          duration: 400,
          easing: 'easeInOutQuad',
        }, '-=300')
      }
    },
    pressSignal() {
      if (this.recordKeyPresses && this.secretAnswer.length < 42) {
        this.secretAnswer += this.lastPressedCharacter
      }
    },
    backspaceSignal() {
      if (this.recordKeyPresses && this.secretAnswer.length > 0) {
        this.secretAnswer = this.secretAnswer.slice(0, this.secretAnswer.length - 1)
      }
    },
    crSignal() {
      if (this.recordKeyPresses) {
        this.validate()
      }
    },
  },
  mounted: function() {
    this.$anime({
      targets: this,
      fullBlockOpacity: 0,
      duration: 500,
      loop: true,
      direction: 'alternate',
      easing: 'easeInOutExpo',
    })
  },
}
</script>