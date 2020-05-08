<template>
  <div class="d-flex h-100 d-flex flex-column mx-3">
    <div class="selector-frame glowing-container position-relative w-100 h-100 mb-4">
      <div class="alpha">{{ $t('α') }}</div>
      <div class="omega">{{ $t('Ω') }}</div>
      <div class="beta-minus">{{ $t('β_minus') }}</div>
      <div class="beta-plus">{{ $t('β_plus') }}</div>

      <DishSelector
        v-for="(item, itemIndex) in menuItems"
        :key="item.id"
        :itemIndex="itemIndex"
      />

      <div v-for="(graduation, graduationIndex) in graduations" :key="graduationIndex"
        class="graduation"
        :style="{
          left: graduation.left,
          bottom: graduation.bottom,
          width: graduation.width,
          height: graduation.height,
          opacity: graduationsOpacity,
        }"
      />

      <div
        v-for="area in selectableAreas" :key="area.id"
        class="selectable-area"
        :style="{
          top: area.top + '%',
          left: area.left + '%',
          height: selectableAreaHeight,
          width: selectableAreaWidth,
          opacity: selectableAreasOpacity,
        }">
      </div>
    </div>

    <div class="d-flex flex-row justify-content-center">
      <div class="button-like-frame generator-matrix-title position-relative">
        {{ $t('dish_generator_matrix') }}
      </div>
    </div>
  </div>
</template>

<script>
import DishSelector from '@/components/DishSelector.vue'
import menuStore from '@/store/menuStore.js'
import difficultyStore from '@/store/difficultyStore.js'

export default {
  name: 'DishMatrix',
  components: {
    DishSelector,
  },
  data() {
    return {
      selectableAreasOpacity: 0,
      graduationsOpacity: 1,
    }
  },
  computed: {
    selectableAreas: function() {
      return menuStore.state.selectableAreas
    },
    selectableAreaWidth: function() {
      return menuStore.state.selectableAreaWidth + '%'
    },
    selectableAreaHeight: function() {
      return menuStore.state.selectableAreaHeight + '%'
    },
    menuItems: function() {
      return menuStore.state.menuItems
    },
    graduations: function() {
      return [
        {
          left: "-5px",
          bottom: "27%",
          height: "1px",
          width: "5px",
        },
        {
          left: "-7px",
          bottom: "50%",
          height: "1px",
          width: "7px",
        },
        {
          left: "-5px",
          bottom: "73%",
          height: "1px",
          width: "5px",
        },
        {
          left: "27%",
          bottom: "-5px",
          height: "5px",
          width: "1px",
        },
        {
          left: "50%",
          bottom: "-7px",
          height: "7px",
          width: "1px",
        },
        {
          left: "73%",
          bottom: "-5px",
          height: "5px",
          width: "1px",
        },
      ]
    },
    difficulty: function() {
      return difficultyStore.state.difficulty
    },
  },
  watch: {
    difficulty: function(newValue) {
      if (newValue == difficultyStore.state.EASY) {
        this.$anime({
          targets: this,
          selectableAreasOpacity: 1,
          duration: 4000,
          easing: 'easeInOutExpo',
        })
      } else {
        this.$anime({
          targets: this,
          selectableAreasOpacity: 0,
          duration: 4000,
          easing: 'easeInOutExpo',
        })
      }

      if (newValue == difficultyStore.state.HARD) {
        this.$anime({
          targets: this,
          graduationsOpacity: 0,
          duration: 4000,
          easing: 'easeInOutExpo',
        })
      } else {
        this.$anime({
          targets: this,
          graduationsOpacity: 1,
          duration: 4000,
          easing: 'easeInOutExpo',
        })
      }
    },
  },
  created() {
    if (this.difficulty == difficultyStore.state.EASY) {
      this.selectableAreasOpacity = 1
      this.graduationsOpacity = 1
    } else if (this.difficulty == difficultyStore.state.NORMAL) {
      this.selectableAreasOpacity = 0
      this.graduationsOpacity = 1
    } else if (this.difficulty == difficultyStore.state.HARD) {
      this.selectableAreasOpacity = 0
      this.graduationsOpacity = 0
    }
  },
}
</script>

<style scoped>
.alpha {
  position: absolute;
  text-align: left;
  left: 0;
  bottom: calc(-20px - 2px);
  line-height: 1;
  font-size: 20px;
  color: rgba(255, 255, 255, 0.65);
}

.omega {
  position: absolute;
  text-align: right;
  right: 0;
  bottom: calc(-20px - 2px);
  line-height: 1;
  font-size: 20px;
  color: rgba(255, 255, 255, 0.65);
}

.beta-minus {
  position: absolute;
  bottom: 0;
  left: calc(-20px - 2px);
  writing-mode: tb-rl;
  transform: rotate(180deg);
  line-height: 1;
  font-size: 20px;
  color: rgba(255, 255, 255, 0.65);
}

.beta-plus {
  position: absolute;
  top: 0;
  left: calc(-20px - 2px);
  writing-mode: tb-rl;
  transform: rotate(180deg);
  line-height: 1;
  font-size: 20px;
  color: rgba(255, 255, 255, 0.65);
}

.selectable-area {
  position: absolute;
  border: 1px dotted rgba(255, 255, 255, 0.7);
  box-shadow: 0px 0px 14px -8px rgba(255, 255, 255, 1);
}

.selector-frame {
  background:
    linear-gradient(to right, transparent 20%, rgba(0, 150, 150, 0.09) 80%),
    linear-gradient(to top, transparent 20%, rgba(0, 150, 150, 0.09) 80%);
}

/* The same padding than on buttons */
.button-like-frame {
  padding: 0.375rem 1rem 0.275rem 1rem;
}

.generator-matrix-title {
  color: rgba(255, 255, 255, 0.65);
  background-color: rgba(00, 45, 80, 0.6);
  /*border: 1px solid rgba(0, 209, 182, 0.55);*/
  font-size: 20px;
  clip-path: polygon(
    10px 0%,
    calc(100% - 10px) 0%,
    100% 10px,
    100% calc(100% - 10px),
    calc(100% - 10px) 100%,
    10px 100%,
    0% calc(100% - 10px),
    0% 10px
  );
}

.generator-matrix-title::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
  background-color: #00d1b6;
  clip-path: polygon(
    10px 0%,
    calc(100% - 10px) 0%,
    100% 10px,
    100% calc(100% - 10px),
    calc(100% - 10px) 100%,
    10px 100%,
    0% calc(100% - 10px),
    0% 10px,
    10px 0%,
    calc(10px + 1px) 1px,
    1.5px calc(10px + 1px),
    1.5px calc(100% - 10px - 1px),
    calc(10px + 1px) calc(100% - 1.5px),
    calc(100% - 10px - 1px) calc(100% - 1.5px),
    calc(100% - 1px) calc(100% - 10px - 1px),
    calc(100% - 1px) calc(10px + 1px),
    calc(100% - 10px - 1px) 1.5px,
    calc(10px + 1px) 1.5px
  );
  z-index: 10;
}

.graduation {
  position: absolute;
  background-color: #00d1b6;
  box-shadow: 0px 1px 3px 0.01px rgba(0, 209, 182, 0.7);
}
</style>