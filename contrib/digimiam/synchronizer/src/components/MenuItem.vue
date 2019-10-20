<template>
  <div class="d-flex flex-row justify-content-between mb-4">
    <div
      :id="animationId"
      class="text font-italic"
      :style="{color: 'rgb(' + dish.color.r + ', ' + dish.color.g + ', ' + dish.color.b + ')'}"
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
    </div>

    <span class="underline-dots flex-grow-1 mx-1"></span>

    <div
      :style="{color: 'rgb(' + price.color.r + ', ' + price.color.g + ', ' + price.color.b + ')'}"
    >
      <span
        v-for="i in price.array"
        :key="i.id"
        :style="{opacity: i.opacity}"
        v-html="i.char"
      ></span>
      <span>Ḟ</span>
    </div>
  </div>
</template>

<script>
import MenuStore from '@/store/MenuStore.js'

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
      price: {
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
    }
  },
  computed: {
    animationId: function() {
      return 'dish' + this.itemIndex
    },
    dishLabel: function() {
      return MenuStore.state.menuItems[this.itemIndex].dish
    },
    priceLabel: function() {
      return MenuStore.state.menuItems[this.itemIndex].price
    },
  },
  methods: {
    glitchAnimation: function() {
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

      this[data].remainingScrambleAnimations = 50
      this[data].arrayPlusMinusCharProba = 0.1

      for (i = 0 ; i < this[data].array.length ; i++) {
        this[data].array[i].scrambleProba = 0.1
        this[data].array[i].finalChar = false
      }

      if (this[data].remainingScrambleAnimations > -1) {
        if (this[data + 'Label'] === null) {
          if (this[data].colorAnimationReverse === false) {
            this[data].colorAnimationReverse = true
            this[data].colorAnimation.reverse()
          }
          if (this[data].colorAnimation.progress > 0) {
            this[data].colorAnimation.play()
          }
        }
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
      }
    },
  },
  watch: {
    dishLabel: function(newValue) {
      if (newValue === null) {
        this.dishColor = 'orangered'
        this.scrambleTo('dish', '## Error ##')
      } else {
        this.dishColor = 'yellow'
        this.scrambleTo('dish', newValue)
      }
    },
    priceLabel: function(newValue) {
      if (newValue === null) {
        this.priceColor = 'orangered'
        this.scrambleTo('price', '??')
      } else {
        this.priceColor = 'yellow'
        this.scrambleTo('price', newValue)
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

    this.price.colorAnimation = this.$anime({
      autoplay: false,
      duration: 500,
      update(anim) {
        this_.price.color.g = 69 + 186 * anim.progress / 100
      },
      easing: 'linear',
    })

    this.glitchAnimation()
    this.scrambleTo('dish', '## Error ##')
    this.scrambleTo('price', '??')
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
  position: relative;
  z-index: 10;
}

.underline-dots {
  border-bottom: 1px dotted #ffffff;
  margin-bottom: 3px;
}
</style>
