<template>
  <div
    class="password-window z-index-20 position-absolute"
    :style="{top: top, left: left, transform: transform}"
  >
    <Window :title="'AUTHENTIFICATION'" theme="warning">
      <div class="d-flex flex-column justify-content-between px-3 py-4 h-100 bg-black-transparent text-orange-light">
        <div class="text-18">
          <div>
            L'ouverture du réseau requiert le mot de passe administrateur.
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
            class="align-self-end text-underline"
          >
            Mot de passe oublié ?
          </div>
        </div>
        <div class="d-flex flex-row justify-content-between">
          <div class="text-red align-self-center" :style="{opacity: errorMessageOpacity}">
            Mot de passe incorrect.
          </div>
          <ButtonOrange @click="validate">
            Valider
          </ButtonOrange>
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
      errorMessageOpacity: 0,
      errorMessageOpacityAnimation: this.$anime({}),
    }
  },
  computed: {
    displayed() {
      return businessStore.state.displayPasswordWindow
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
      this.errorMessageOpacityAnimation.pause()
      this.errorMessageOpacity = 1
      this.errorMessageOpacityAnimation = this.$anime({
        targets: this,
        errorMessageOpacity: 0,
        duration: 7000,
        easing: 'easeInQuad',
      })
      this.password = ''
    },
    displayPasswordRecoveryWindow() {
      businessStore.state.displayPasswordRecoveryWindow = true
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