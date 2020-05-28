<template>
  <div class="d-flex h-100 d-flex flex-column mx-3">
    <div class="selector-frame glowing-container position-relative w-100 h-100 mb-4">

      <DishSelector
        v-for="(item, itemIndex) in menuItems"
        :key="item.id"
        :itemIndex="itemIndex"
      />

      <DishMatrixGraduation
        v-for="(graduation, graduationIndex) in graduations" :key="graduationIndex"
        :dashLeft="graduation.dashLeft"
        :dashBottom="graduation.dashBottom"
        :dashWidth="graduation.dashWidth"
        :dashHeight="graduation.dashHeight"
        :icon="graduation.icon"
        :iconFa="graduation.iconFa"
        :iconLeft="graduation.iconLeft"
        :iconBottom="graduation.iconBottom"
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
import DishMatrixGraduation from '@/components/DishMatrixGraduation.vue'
import DishSelector from '@/components/DishSelector.vue'
import menuStore from '@/store/menuStore.js'
import difficultyStore from '@/store/difficultyStore.js'

export default {
  name: 'DishMatrix',
  components: {
    DishMatrixGraduation,
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
      return menuStore.state.graduations
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
  top: 15px;
  color: rgba(255, 255, 255, 0.65);
  background-color: rgba(00, 45, 80, 0.6);
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
    calc(10px + 1.5px) 1px,
    1.5px calc(10px + 1px),
    1.5px calc(100% - 10px - 1px),
    calc(10px + 1px) calc(100% - 1.5px),
    calc(100% - 10px - 1px) calc(100% - 1.5px),
    calc(100% - 1.5px) calc(100% - 10px - 1px),
    calc(100% - 1.5px) calc(10px + 1px),
    calc(100% - 10px - 1px) 1.5px,
    calc(10px + 1px) 1.5px
  );
  z-index: 10;
}
</style>