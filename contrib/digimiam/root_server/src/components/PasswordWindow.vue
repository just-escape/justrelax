<template>
  <div
    class="password-window z-index-20 position-absolute"
    :style="{top: top, left: left, transform: transform}"
  >
    <Window :title="$t('authentication')" theme="warning">
      <div class="d-flex flex-column justify-content-between px-3 py-4 h-100 bg-black-transparent text-orange-light">
        <div class="text-18">
          <div>
            {{ $t('password_required') }}
          </div>
        </div>
        <div class="d-flex flex-column">
          <div
            class="text-18 input-warning mb-2 p-1 rounded"
          >
            <span v-html="password"/>
            <span
              v-if="recordKeyPresses"
              :style="{
                opacity: fullBlockOpacity,
              }"
            >&#9608;</span>
          </div>
          <div
            @click="displayPasswordRecoveryWindow"
            class="align-self-end text-underline position-relative"
          >
            {{ $t('forgot_your_password') }}
            <div :class="{pulsate: (failedAttempts >= 2 || forcePulsate) && !isRecoveryWindowDisplayed}"></div>
          </div>
        </div>
        <div class="d-flex flex-row justify-content-between">
          <div class="text-red align-self-center" :style="{opacity: errorMessageOpacity}">
            <div>
              {{ $t('incorrect_password') }}
            </div>
            <div>
              {{ $t("Nombre d'échecs :") }} {{ failedAttempts }}.
            </div>
          </div>
          <div>
            <ButtonOrange @click="validate" class="mr-4" >
              {{ $t('confirm') }}
            </ButtonOrange>
            <ButtonOrange @click="hidePasswordWindow">
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
  name: "PasswordWindow",
  components: {
    Window,
    ButtonOrange,
  },
  data() {
    return {
      topOffset: 200,
      leftOffset: 400,
      scaleX: 0,
      scaleY: 0,
      password: '',
      fullBlockOpacity: 1,
      failedAttempts: 0,
      errorMessageOpacity: 0,
      errorMessageOpacityAnimation: this.$anime({}),
      forcePulsate: false,
    }
  },
  computed: {
    displayed() {
      return businessStore.state.displayPasswordWindow
    },
    isRecoveryWindowDisplayed() {
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
      return businessStore.state.displayPasswordWindow && !businessStore.state.displayPasswordRecoveryWindow
    },
  },
  methods: {
    validate() {
      this.failedAttempts++
      this.errorMessageOpacityAnimation.pause()
      this.errorMessageOpacity = 1
      this.errorMessageOpacityAnimation = this.$anime({
        targets: this,
        errorMessageOpacity: 0,
        duration: 7000,
        easing: 'easeInQuad',
      })
      this.password = ''
      businessStore.commit('passwordTry', this.password)
      if (this.failedAttempts == 3) {
        this.displayPasswordRecoveryWindow()
      }
    },
    setForcePulsate(value) {
      this.forcePulsate = value
    },
    displayPasswordRecoveryWindow() {
      businessStore.state.displayPasswordRecoveryWindow = true
    },
    hidePasswordWindow() {
      businessStore.commit('hidePasswordWindow')
      setTimeout(businessStore.commit, 500, 'displayPasswordWindow')
    },
  },
  watch: {
    displayed(newValue) {
      if (newValue) {
        setTimeout(this.setForcePulsate, 25000, true)
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
          leftOffset: 70,
          topOffset: 300,
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
          topOffset: 200,
          duration: 400,
          easing: 'easeInOutQuad',
        }, '-=300')
      }
    },
    pressSignal() {
      if (this.recordKeyPresses && this.password.length < 42) {
        this.password += '•'
      }
    },
    backspaceSignal() {
      if (this.recordKeyPresses && this.password.length > 0) {
        this.password = this.password.slice(0, this.password.length - 1)
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

<style scoped>
.pulsate {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  background: #fd7e14;
  animation: pulser 1.4s linear infinite;
  opacity: 0;
}

@keyframes pulser {
	0% {
		transform: scale(1);
		opacity: 0;
	}
  20% {
		transform: scale(1);
		opacity: 0;
	}
	60% {
		transform: scale(1.4);
		opacity: 0.4;
	}
	100% {
		transform: scale(1.50);
		opacity: 0;
	}
}
</style>