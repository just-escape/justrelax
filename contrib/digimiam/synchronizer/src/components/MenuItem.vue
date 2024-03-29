<template>
  <div class="d-flex flex-row justify-content-between mb-4">
    <div
      :id="animationId"
      class="text font-italic position-relative"
      :style="{
        color: isDishValidated ? 'green' : 'rgb(' + dish.color.r + ', ' + dish.color.g + ', ' + dish.color.b + ')',
        transition: isDishValidated ? 'color 2s ease-in-out' : '',
      }"
    >
      <div class="d-flex flex-row collision-tutor">
        <span
          v-for="i in dish.array"
          :key="i.id"
          v-html="i.char"
        ></span>
      </div>
      <div
        class="d-flex flex-row glitch top"
        :class="{'red-shadow': redShadow}"
      >
        <span
          v-for="i in dish.array"
          :key="i.id"
          :style="{opacity: i.opacity}"
          v-html="i.char"
        ></span>
      </div>
      <div
        class="d-flex flex-row glitch bottom"
        :class="{'red-shadow': redShadow}"
      >
        <span
          v-for="i in dish.array"
          :key="i.id"
          :style="{opacity: i.opacity}"
          v-html="i.char"
        ></span>
      </div>
      <div
        class="position-absolute badge text-teal"
        style="right: -60px; font-size: 12px; background: rgba(0, 45, 80, 1); border: 1px solid rgba(0, 209, 182, 0.7); font-weight: normal"
        :style="{opacity: notifOpacity, bottom: notifBottom + 'px'}"
      >
        hologramme<br/>uploadé
      </div>
    </div>

    <span class="underline-dots flex-grow-1 mx-1"></span>

    <div
      class="price"
      :style="{
        color: isDishValidated ? 'green' : 'rgb(' + dish.color.r + ', ' + dish.color.g + ', ' + dish.color.b + ')',
        transition: isDishValidated ? 'color 2s ease-in-out' : '',
      }"
    >
      {{ price }} NéoFrancs
    </div>
  </div>
</template>

<script>
import menuStore from '@/store/menuStore.js'

export default {
  name: 'MenuItem',
  data: function() {
    return {
      scrambleChars: '!<>-_\\/[]{}—=+*^?#________',
      redShadow: false,
      dish: {
        // -1 => is not animated
        remainingScrambleAnimations: -1,
        targetChars: [],
        arrayPlusMinusCharProba: 0,
        array: [],
        colorAnimation: null,
        colorAnimationReverse: false,
        color: {
          r: 255,
          g: 69,
          b: 0,
        },
      },
      notifOpacity: 0,
      notifBottom: 0,
    }
  },
  computed: {
    animationId: function() {
      return 'dish' + this.itemIndex
    },
    dishLabel: function() {
      return menuStore.state.menuItems[this.itemIndex].dish
    },
    price: function() {
      return menuStore.state.menuItems[this.itemIndex].price
    },
    cursorPosition: function() {
      return menuStore.state.menuItems[this.itemIndex].cursorLeft + '-' + menuStore.state.menuItems[this.itemIndex].cursorTop
    },
    lang: function() {
      return this.$i18n.locale
    },
    isDishValidated: function() {
      return menuStore.state.menuItems[this.itemIndex].isDishValidated
    },
  },
  methods: {
    createNotif() {
      this.$anime.timeline({
        targets: this,
      })
      .add({
        notifOpacity: 1,
        duration: 80,
        easing: 'linear',
      })
      .add({
        notifBottom: 20,
        notifOpacity: 0,
        duration: 1000,
        easing: 'easeInOutQuad',
      }, '+=500')
      .add({
        notifBottom: 0,
        duration: 1,
      }, '+=100')
    },
    glitchAnimation: function() {
      if (this.isDishValidated) {
        return
      }

      var this_ = this

      this.$anime.timeline({})
      .add({
        targets: '#' + this.animationId + ' .glitch',
        duration: 100,
        skewX: 70,
        easing: 'easeInOutQuad',
      })
      .add({
        targets: '#' + this.animationId + ' .glitch',
        duration: 30,
        skewX: 0,
        easing: 'easeInOutQuad',
      })
      .add({
        targets: '#' + this.animationId + ' .glitch',
        duration: 30,
        opacity: 0,
        easing: 'linear',
      })
      .add({
        targets: '#' + this.animationId + ' .glitch',
        duration: 30,
        opacity: 1,
        easing: 'linear',
      })
      .add({
        targets: '#' + this.animationId + ' .glitch',
        duration: 30,
        translateX: -5,
        easing: 'linear',
      })
      .add({
        targets: '#' + this.animationId + ' .glitch',
        duration: 30,
        translateX: 5,
        easing: 'linear',
      })
      .add({
        targets: '#' + this.animationId + ' .top',
        duration: 80,
        translateX: -2,
        easing: 'easeInOutQuad',
      })
      .add({
        targets: '#' + this.animationId + ' .bottom',
        duration: 80,
        translateX: 2,
        easing: 'easeInOutQuad',
      }, '-=80')
      .add({
        targets: '#' + this.animationId + ' .text',
        duration: 1,
        scale: 1.05,
        easing: 'linear',
      }, '-=80')
      .add({
        targets: '#' + this.animationId + ' .text',
        duration: 1,
        scale: 1,
        easing: 'linear',
      }, '+=20')
      .add({
        duration: 1,
        update: function() {
          this_.redShadow = true
        },
      }, '-=60')
      .add({
        targets: '#' + this.animationId + ' .top',
        duration: 80,
        translateX: 0,
        easing: 'easeInOutQuad',
      })
      .add({
        targets: '#' + this.animationId + ' .bottom',
        duration: 80,
        translateX: 0,
        easing: 'easeInOutQuad',
      }, '-=80')
      .add({
        duration: 1,
        update: function() {
          this_.redShadow = false
        },
      })
      .add({
        targets: '#' + this.animationId + ' .glitch',
        duration: 40,
        scaleY: 1.2,
        easing: 'easeInOutQuad',
      }, '+=800')
      .add({
        targets: '#' + this.animationId + ' .glitch',
        duration: 20,
        scaleY: 1,
        easing: 'easeInOutQuad',
      })

      // delay between 2000 and 20000 ms
      var delay = Math.random() * 18000 + 2000
      setTimeout(this.glitchAnimation, delay)
    },
    randomChar: function() {
      return this.scrambleChars[Math.floor(Math.random() * this.scrambleChars.length)]
    },
    scrambleTo: function(data, target) {
      var i = 0

      this[data].targetChars = []
      for (i = 0 ; i < target.length ; i++) {
        if (target[i] == ' ') {
          this[data].targetChars.push('&nbsp;')
        } else {
          this[data].targetChars.push(target[i])
        }
      }

      if (this[data].remainingScrambleAnimations == -1) {
        var startAnimation = true
      }

      this[data].remainingScrambleAnimations = 50
      this[data].arrayPlusMinusCharProba = 0.1

      for (i = 0 ; i < this[data].array.length ; i++) {
        this[data].array[i].scrambleProba = 0.1
        this[data].array[i].finalChar = false
      }

      if (this[data + 'Label'] === null) {
        if (this[data].colorAnimationReverse === false) {
          this[data].colorAnimationReverse = true
          this[data].colorAnimation.reverse()
        }
        if (this[data].colorAnimation.progress > 0) {
          this[data].colorAnimation.play()
        }
      }

      if (startAnimation) {
        this.scrambleAnimation(data)
      }
    },
    scrambleAnimation: function(data) {
      var i = 0
      var lenDiff = this[data].targetChars.length - this[data].array.length

      if (this[data].remainingScrambleAnimations > 0) {
        if (lenDiff != 0) {
          if (Math.random() < this[data].arrayPlusMinusCharProba) {
            if (lenDiff > 0) {
              this[data].array.push(
                {
                  char: ' ',
                  opacity: 0.5,
                  scrambleProba: 0.9,
                  scrambling: true,
                  finalChar: false,
                }
              )
            } else {
              this[data].array.pop()
            }
            this[data].arrayPlusMinusCharProba = 0.1
          } else {
            this[data].arrayPlusMinusCharProba += 0.05
          }
        }

        for (i = 0 ; i < this[data].array.length ; i++) {
          if (this[data].array[i].finalChar) {
            continue
          }

          if (Math.random() < this[data].array[i].scrambleProba) {
            this.$set(this[data].array[i], 'char', this.randomChar())
            this.$set(this[data].array[i], 'opacity', 0.5)

            if (this[data].array[i].scrambling) {
              this[data].array.scrambleProba -= 0.1
            } else {
              this[data].array.scrambleProba = 0.7
              this[data].array.scrambling = true
            }
          } else {
            if (i < this[data].targetChars.length) {
              if (Math.random() < 1 / this[data].remainingScrambleAnimations) {
                this[data].array[i].char = this[data].targetChars[i]
                this[data].array[i].opacity = 1
                this[data].array[i].scrambleProba = 0
                this[data].array[i].scrambling = false
                this[data].array[i].finalChar = true
              }
            }
          }
        }

        this[data].remainingScrambleAnimations -= 1
        setTimeout(this.scrambleAnimation, 40, data)
      } else {
        if (lenDiff > 0) {
          for (i = 0 ; i < lenDiff ; i++) {
            this[data].array.push({})
          }
        } else if (lenDiff < 0) {
          for (i = 0 ; i < lenDiff ; i++) {
            this[data].array.pop()
          }
        }

        for (i = 0 ; i < this[data].array.length ; i++) {
          if (this[data].remainingScrambleAnimations <= 0) {
            this[data].array[i].char = this[data].targetChars[i]
            this[data].array[i].opacity = 1
            this[data].array[i].scrambleProba = 0
            this[data].array[i].scrambling = false
            this[data].array[i].finalChar = true
          }
        }


        if (this[data + 'Label'] !== null) {
          if (this[data].colorAnimationReverse === true) {
            this[data].colorAnimationReverse = false
            this[data].colorAnimation.reverse()
          }
          this[data].colorAnimation.play()
        }
        this[data].remainingScrambleAnimations -= 1

        if (this.dishLabel !== null) {
          this.createNotif()
        }
        menuStore.commit("pushMenuEntry", {itemIndex: this.itemIndex, onManualMode: false, getters: menuStore.getters})
      }
    },
  },
  watch: {
    dishLabel: function(newValue) {
      if (newValue === null) {
        this.dishColor = 'orangered'
        this.scrambleTo('dish', this.$t('hashtag_hashtag_error'))
      } else {
        this.dishColor = 'yellow'
        this.scrambleTo('dish', this.$t(newValue))
      }
    },
    cursorPosition: function() {
      if (this.dishLabel === null) {
        this.scrambleTo('dish', this.$t('hashtag_hashtag_error'))
      }
    },
    lang: function() {
      if (this.dishLabel === null) {
        this.scrambleTo('dish', this.$t('hashtag_hashtag_error'))
      } else {
        this.scrambleTo('dish', this.$t(this.dishLabel))
      }
    },
  },
  mounted() {
    var this_ = this
    this.dish.colorAnimation = this.$anime({
      autoplay: false,
      duration: 500,
      update(anim) {
        this_.dish.color.g = 69 + 186 * anim.progress / 100
      },
      easing: 'linear',
    })

    this.glitchAnimation()
    this.scrambleTo('dish', this.$t('hashtag_hashtag_error'))
  },
  props: ['itemIndex']
}
</script>

<style scoped>
.collision-tutor {
  color: transparent;
}

.bottom {
  clip-path: inset(58% 0 0 0);
}

.top {
  clip-path: inset(0 0 41% 0);
}

.red-shadow {
  text-shadow: -2px 0 red;
}

.glitch {
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
}

.text {
  font-size: 18px;
  position: relative;
  z-index: 10;
}

.price {
  font-size: 18px;
}
</style>
