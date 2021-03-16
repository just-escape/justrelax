<template>
  <div class="position-relative">
    <div
      class="position-absolute info-shadow rounded-bottom d-flex flex-column align-items-center patterns"
      style="right: 175px; bottom: -245px; width: 40px; z-index: 16"
      :style="{
        height: 'calc(9 * ' + itemHeight + 'px)',
        clipPath: 'polygon(0% calc(200%/9 + ' + 200/9 * patternsVisibility + '%), 100% calc(200%/9 + ' + 200/9 * patternsVisibility + '%), 100% calc(700%/9 - ' + 200/9 * patternsVisibility + '%), 0% calc(700%/9 - ' + 200/9 * patternsVisibility + '%)',
        overflowY: selecting ? 'scroll' : 'hidden',
        maskImage: 'linear-gradient(to bottom, transparent calc(200%/9), transparent ' + (200/9 + 200/9 * patternsVisibility) + '%, black calc(400%/9), black calc(500%/9), transparent ' + (700/9 - 200/9 * patternsVisibility) + '%)'
      }"
      ref="patternsContainer"
      @scroll="scroll()"
    >
      <div
        v-for="(pattern, index) in dynamicPatterns" :key="index"
        @mousedown="mousedown(pattern, false)"
        :class="{rounded: patternsVisibility == 1, 'bg-info': !gray, 'bg-secondary': gray}"
        :style="{'opacity': clickable ? 0.75 : 0.4}"
        style="padding: 6px 8px"
      >
        <img :style="{transform: pattern == selectedPatternId ? 'scale(' + selectedScale + ')' : ''}" :src="patterns[pattern]" height="26px" width="26px">
      </div>
    </div>
  </div>
</template>

<script>
import orderStore from '@/store/orderStore.js'

export default {
  name: "WaffrescoCustomizer",
  data() {
    return {
      selectedScale: 1,
      patternsVisibility: 1,
      selecting: false,
      itemHeight: 38,
      animation: false,
      dynamicPatterns: [],
    }
  },
  computed: {
    patterns() {
      return orderStore.state.waffrescoVariations
    },
    selectedPatternId() {
      return orderStore.state.selectedWaffrescoPatternId
    },
  },
  methods: {
    setAnimationFalse() {
      this.animation = false
    },
    mousedown(newPatternId, force) {
      if (!force && (this.animation || !this.clickable)) {
        return
      }

      this.animation = true
      this.selecting = !this.selecting
      orderStore.commit('setSelectedWaffrescoPatternId', newPatternId)

      let timeline = this.$anime.timeline({
        targets: this,
        easing: 'easeOutCubic',
      })
      .add({
        selectedScale: 1.2,
        duration: 200,
      })
      .add({
        selectedScale: 1,
        duration: 200,
      })

      if (this.selecting) {
        timeline
        .add({
          patternsVisibility: 0,
          duration: 400,
        })
        setTimeout(this.setAnimationFalse, 800)
      } else {
        let itemIndex = 4  // Default just in case, even if the value should always change in the for loop below
        for (let [patternIndex, patternId] of Object.values(this.dynamicPatterns).entries()) {
          if (patternId === newPatternId) {
            itemIndex = patternIndex
          }
        }

        if (itemIndex == 2) {
          this.dynamicPatterns.unshift(this.dynamicPatterns.pop())
          this.$refs.patternsContainer.scrollTop += this.itemHeight
          this.dynamicPatterns.unshift(this.dynamicPatterns.pop())
          this.$refs.patternsContainer.scrollTop += this.itemHeight
          this.dynamicPatterns.unshift(this.dynamicPatterns.pop())
          this.$refs.patternsContainer.scrollTop += this.itemHeight
          itemIndex = 5
        } else if (itemIndex == 3) {
          this.dynamicPatterns.unshift(this.dynamicPatterns.pop())
          this.$refs.patternsContainer.scrollTop += this.itemHeight
          this.dynamicPatterns.unshift(this.dynamicPatterns.pop())
          this.$refs.patternsContainer.scrollTop += this.itemHeight
          itemIndex = 5
        } else if (itemIndex == 4) {
          this.dynamicPatterns.unshift(this.dynamicPatterns.pop())
          this.$refs.patternsContainer.scrollTop += this.itemHeight
          itemIndex = 5
        } else if (itemIndex == this.dynamicPatterns.length - 5) {
          this.dynamicPatterns.push(this.dynamicPatterns.shift())
          this.$refs.patternsContainer.scrollTop -= this.itemHeight
          itemIndex = 6
        } else if (itemIndex == this.dynamicPatterns.length - 4) {
          this.dynamicPatterns.push(this.dynamicPatterns.shift())
          this.$refs.patternsContainer.scrollTop -= this.itemHeight
          this.dynamicPatterns.push(this.dynamicPatterns.shift())
          this.$refs.patternsContainer.scrollTop -= this.itemHeight
          itemIndex = 6
        } else if (itemIndex == this.dynamicPatterns.length - 3) {
          this.dynamicPatterns.push(this.dynamicPatterns.shift())
          this.$refs.patternsContainer.scrollTop -= this.itemHeight
          this.dynamicPatterns.push(this.dynamicPatterns.shift())
          this.$refs.patternsContainer.scrollTop -= this.itemHeight
          this.dynamicPatterns.push(this.dynamicPatterns.shift())
          this.$refs.patternsContainer.scrollTop -= this.itemHeight
          itemIndex = 6
        }

        let scrollTarget = this.itemHeight * (itemIndex - 4)
        timeline
        .add({
          targets: this.$refs.patternsContainer,
          scrollTop: scrollTarget,
          duration: 300,
          easing: 'easeOutQuad',
        }, '-=200')
        .add({
          patternsVisibility: 1,
          duration: 400,
        })
        setTimeout(this.setAnimationFalse, 900)
      }
    },
    scroll() {
      if (this.selecting) {
        // Ensures infinite scrolling
        if (this.$refs.patternsContainer.scrollTop == 0) {
          this.dynamicPatterns.unshift(this.dynamicPatterns.pop())
          this.$refs.patternsContainer.scrollTop += this.itemHeight
        } else if (this.$refs.patternsContainer.scrollTop + this.$refs.patternsContainer.offsetHeight == this.$refs.patternsContainer.scrollHeight) {
          this.dynamicPatterns.push(this.dynamicPatterns.shift())
          this.$refs.patternsContainer.scrollTop -= this.itemHeight
        }
      }
    },
    reloadPatterns() {
      this.dynamicPatterns = []
      for (let pattern in this.patterns) {
        if (pattern !== this.selectedPatternId) {
          this.dynamicPatterns.push(pattern)
        }
      }
      // Ensures the selected pattern is initially at the good position
      this.dynamicPatterns.splice(4, 0, this.selectedPatternId)
    }
  },
  watch: {
    collapseSignal() {
      if (this.selecting) {
        this.mousedown(this.dynamicPatterns[Math.round(this.$refs.patternsContainer.scrollTop / this.itemHeight) + 4], true)
      }
    },
  },
  mounted() {
    this.reloadPatterns()
  },
  props: {
    clickable: Boolean,
    gray: Boolean,
    collapseSignal: String,
  }
}
</script>

<style scoped>
.patterns::-webkit-scrollbar {
  display: none;
}
</style>
