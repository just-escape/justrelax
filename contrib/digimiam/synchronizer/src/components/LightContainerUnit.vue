<template>
  <div v-if="color === 'black'" class="d-flex flex-row justify-content-center align-items-center">
    <img style="font-size: 200px; margin-top: 40px" src="@/assets/img/green-sun.svg" height="200px"/>
  </div>
  <div v-else>
    <div class="position-relative">
      <div class="page position-absolute" style="left: 30px">
        <div class="hal d-flex">
          <div class="hal-eye -circular">
            <div class="position-absolute" style="top: -30px; left: -30px">
              <div class="progress-circle">
                <div
                  class="progress-mask"
                  :style="{clip: completeness > 50 ? 'rect(auto, auto, auto, auto)' : 'rect(0, 330px, 330px, 165px)'}"
                >
                  <div
                    class="progress-bar"
                    :style="{
                      transform: 'rotate(' + 360 * Math.min(50, completeness) / 100 + 'deg)',
                      filter: hueRotate ? 'hue-rotate(-40deg) brightness(0.65) contrast(0.95)' : '',
                    }"
                  ></div>
                  <div
                    class="progress-bar-sup-50"
                    :style="{
                      display: completeness > 50 ? 'block' : 'none',
                      transform: 'rotate(' + 360 * Math.min(50, completeness - 50) / 100 + 'deg)',
                      filter: hueRotate ? 'hue-rotate(-40deg) brightness(0.65) contrast(0.95)' : '',
                    }"
                  ></div>
                </div>
              </div>
            </div>
            <div class="__ring -circular"></div>
            <div class="__oculus -circular">
              <div class="__iris -circular -narrow" :style="{background: coloredGradient}"></div>
              <div class="__iris -circular -wide" :style="{background: coloredGradient}"></div>
              <div class="__highlight -alpha"></div>
              <div class="__highlight -beta"></div>
              <div class="__highlight -gamma"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import lightStore from '@/store/lightStore.js'

export default {
  name: 'LightContainerUnit',
  data() {
    return {
      colors: {
        red: "rgb(220, 53, 69)",
        white: "rgb(255, 255, 255)",
        pink: "rgb(232, 62, 140)",
        green: "rgb(40, 167, 69)",
        blue: "rgb(0, 170, 255)",
        orange: "rgb(253, 126, 20)",
        black: "rgb(0, 0, 0)",
      },
      hueRotate: false,
    }
  },
  computed: {
    coloredGradient() {
      return "-webkit-radial-gradient(center center, circle cover, " + this.colors[this.color] + " 20%, #000000 55%, #000000 85%)"
    },
    isColorActivated() {
      return lightStore.state.activatedSensors[this.color]
    },
    activationSpeed() {
      let counter = 0
      for (let k in lightStore.state.activatedSensors) {
        if (lightStore.state.activatedSensors[k]) {
          counter += 1
        }
      }

      if (this.color === "pink") {
        if (counter === 4) {
          return 8
        } else if (counter === 5) {
          return 16
        } else if (counter === 6) {
          return 32
        } else {
          return 4
        }
      } else {
        if (counter === 2) {
          return 8
        } else if (counter === 3) {
          return 16
        } else if (counter >= 4) {
          return 32
        } else {
          return 4
        }
      }
    },
  },
  methods: {
    updateCompleteness(wasColorActivated) {
      if (this.activable) {
        let delta
        if (wasColorActivated && this.isColorActivated) {
          delta = 100 / 30 / this.activationSpeed
        } else {
          delta = -1 * 100 / 30 / 32
        }
        lightStore.commit('updateCompleteness', {sequenceId: this.id, deltaCompleteness: delta})

        setTimeout(this.updateCompleteness, 1 / 60 * 1000, this.isColorActivated)
      }
    },
    setHueRotateTrue() {
      this.hueRotate = true
    }
  },
  watch: {
    activable(newValue) {
      if (newValue) {
        this.updateCompleteness(this.isColorActivated)
      }
    },
    completeness(newValue) {
      if (newValue === 100) {
        setTimeout(lightStore.commit, 1200, 'next')
        setTimeout(this.setHueRotateTrue, 3000)
      }
    },
  },
  mounted() {
    if (this.activable) {
      this.updateCompleteness(this.isColorActivated)
    }
  },
  props: {
    id: {
      type: Number,
    },
    color: {
      type: String,
      default: "blue",
    },
    completeness: {
      type: Number,
      default: 0,
    },
    activable: {
      type: Boolean,
      default: false,
    }
  }
}
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.page {
  height: 100%;
  width: 100%;
}

/*@keyframes pulse {
  0% {
    opacity: 1;
  }

  100% {
    opacity: 0;
  }
}*/

.-circular, .hal-eye .__ring:before, .hal-eye .__oculus .__iris {
  border-radius: 100%;
}

.hal {
  position: relative;
}

.hal-eye {
  height: 270px;
  width: 270px;
  bottom: calc(-197px - 135px);
  position: absolute;
}

.hal-eye .__ring {
  height: 100%;
  padding: 0.5em;
  position: relative;
  background: rgba(0, 209, 182, 1);
}

.hal-eye .__ring:before {
  content: '';
  display: block;
  height: 100%;
  width: 100%;
  background: rgba(0, 45, 80, 0.7);
}

.hal-eye .__oculus {
  background-color: #000;
  border: 1px solid rgba(0, 0, 0, 0.5);
  height: 80%;
  left: 50%;
  margin: -40% 0 0 -40%;
  /*overflow: hidden;*/
  position: absolute;
  top: 50%;
  width: 80%;
}

.hal-eye .__oculus .__iris {
  content: '';
  display: block;
  height: 100%;
  width: 100%;
  position: absolute;
}

.hal-eye .__oculus .__iris.-wide {
  animation: pulse 2s ease-in-out infinite alternate;
}

.hal-eye .__highlight {
  background-color: rgba(255, 255, 255, 0.12);
  border-radius: 100%;
  height: 8%;
  left: 50%;
  margin-left: -12%;
  position: absolute;
  top: 6%;
  width: 24%;
}

.hal-eye .__highlight:before, .hal-eye .__highlight:after {
  border-radius: 100%;
  left: 50%;
  position: absolute;
}

.hal-eye .__highlight:before {
  content: '';
  display: block;
  height: 50%;
  width: 50%;
  background-color: rgba(255, 255, 255, 0.1);
  margin-left: -25%;
  top: 130%;
}

.hal-eye .__highlight:after {
  content: '';
  display: block;
  height: 26%;
  width: 26%;
  background-color: rgba(255, 255, 255, 0.1);
  margin-left: -13%;
  top: 250%;
}

.hal-eye .__highlight.-alpha {
  left: 75%;
  margin-left: 0;
  top: 30%;
  transform: rotate(60deg);
}

.hal-eye .__highlight.-gamma {
  left: 2%;
  margin-left: 0;
  top: 30%;
  transform: rotate(-60deg);
}

.progress-circle {
  position: relative;
  box-sizing: border-box;
  width: 330px;
  height: 330px;
  border-radius: 50%;
}

.progress-mask {
  position: absolute;
  width: 330px;
  height: 330px;
}

.progress-bar,
.progress-bar-sup-50 {
  position: absolute;
  border-radius: 50%;
  width: 330px;
  height: 330px;
  background: rgb(0, 209, 182);
  transition: filter 0.8s ease-in-out;
}

.progress-bar {
  clip: rect(0, 165px, 330px, 0);
}

.progress-bar-sup-50 {
  clip: rect(0, 330px, 330px, 165px);
}
</style>