<template>
  <div class="d-flex h-100 d-flex flex-column mx-3">
    <div class="selector-frame glowing-container position-relative w-100 h-100 mb-4">

      <DishSelector
        v-for="(item, itemIndex) in menuItems"
        :key="item.id"
        :itemIndex="itemIndex"
      />

      <div class="position-absolute d-flex flex-row w-100" style="top: calc(100% + 1px); transition: opacity 4s ease-in-out" :style="{opacity: displayGraduations ? 1 : 0}">
        <div class="position-relative w-25 text-center">
          <div class="position-absolute dash dash-vertical"></div>
          <div class="mt-2">
            <i class="fa-fw fas fa-drumstick-bite" :class="{'mr-1': displayGraduationTexts}" style="opacity: 0.7"/>
            <span v-if="displayGraduationTexts">Viande</span>
          </div>
        </div>
        <div class="position-relative w-25 text-center">
          <div class="position-absolute dash dash-vertical"></div>
          <div class="mt-2">
            <i class="fa-fw fas fa-pizza-slice" :class="{'mr-1': displayGraduationTexts}" style="opacity: 0.7"/>
            <span v-if="displayGraduationTexts">Pizza</span>
          </div>
        </div>
        <div class="position-relative w-25 text-center">
          <div class="position-absolute dash dash-vertical"></div>
          <div class="mt-2">
            <img src="@/assets/img/waffle.png" :class="{'mr-1': displayGraduationTexts}" style="opacity: 0.7" height="16px"/>
            <span v-if="displayGraduationTexts">Gaufre</span>
          </div>
        </div>
        <div class="position-relative w-25 text-center">
          <div class="position-absolute dash dash-vertical"></div>
          <div class="mt-2">
            <img src="@/assets/img/jelly.svg" :class="{'mr-1': displayGraduationTexts}" style="opacity: 0.7" height="16px"/>
            <span v-if="displayGraduationTexts">Gelée</span>
          </div>
        </div>
      </div>

      <div class="position-absolute d-flex flex-column h-100" style="left: -11px; width: 10px; transition: opacity 4s ease-in-out" :style="{opacity: displayGraduations ? 1 : 0}">
        <div class="position-relative h-25 d-flex">
          <div class="position-absolute dash dash-horizontal"></div>
          <div class="position-absolute h-100 d-flex justify-content-center" style="writing-mode: vertical-lr; transform: rotate(180deg); left: -20px">
            <i
              class="fa-fw fas fa-smile" :class="{'ml-1': displayGraduationTexts}"
              style="opacity: 0.7" :style="{transform: displayGraduationTexts ? 'rotate(90deg)' : 'rotate(-180deg)'}"
            />
            <div v-if="displayGraduationTexts" :class="{'mt-1': displayGraduationTexts}">Portrait</div>
          </div>
        </div>
        <div class="position-relative h-25 text-center">
          <div class="position-absolute dash dash-horizontal"></div>
          <div class="position-absolute h-100 d-flex justify-content-center" style="writing-mode: vertical-lr; transform: rotate(180deg); left: -20px">
            <i
              class="fa-fw fas fa-bug" :class="{'ml-1': displayGraduationTexts}"
              style="opacity: 0.7" :style="{transform: displayGraduationTexts ? 'rotate(90deg)' : 'rotate(-180deg)'}"
            />
            <div v-if="displayGraduationTexts" :class="{'mt-1': displayGraduationTexts}">Insecte</div>
          </div>
        </div>
        <div class="position-relative h-25 text-center">
          <div class="position-absolute dash dash-horizontal"></div>
          <div class="position-absolute h-100 d-flex justify-content-center" style="writing-mode: vertical-lr; transform: rotate(180deg); left: -20px">
            <i
              class="fa-fw fas fa-search" :class="{'ml-1': displayGraduationTexts}"
              style="opacity: 0.7" :style="{transform: displayGraduationTexts ? 'rotate(90deg)' : 'rotate(-180deg)'}"
            />
            <div v-if="displayGraduationTexts" :class="{'mt-1': displayGraduationTexts}">Micro-</div>
          </div>
        </div>
        <div class="position-relative h-25 text-center">
          <div class="position-absolute dash dash-horizontal"></div>
          <div class="position-absolute h-100 d-flex justify-content-center" style="writing-mode: vertical-lr; transform: rotate(180deg); left: -20px">
            <img
              src="@/assets/img/seaweed.png" height="16px"
              :class="{'mb-1': displayGraduationTexts}" style="opacity: 0.7" :style="{transform: displayGraduationTexts ? 'rotate(90deg)' : 'rotate(-180deg)'}"
            />
            <div v-if="displayGraduationTexts" :class="{'mt-1': displayGraduationTexts}">Algue</div>
          </div>
        </div>
      </div>

      <div
        v-for="area in selectableAreas" :key="area.id"
        class="selectable-area"
        style="transition: opacity 4s ease-in-out"
        :style="{
          top: area.top + '%',
          left: area.left + '%',
          height: selectableAreaHeight,
          width: selectableAreaWidth,
          opacity: displaySelectableAreas ? 1 : 0,
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
  computed: {
    displaySelectableAreas() {
      return menuStore.state.displaySelectableAreas
    },
    displayGraduations() {
      return menuStore.state.displayGraduations
    },
    displayGraduationTexts() {
      return menuStore.state.displayGraduationTexts
    },
    selectableAreas() {
      return menuStore.state.selectableAreas
    },
    selectableAreaWidth() {
      return menuStore.state.selectableAreaWidth + '%'
    },
    selectableAreaHeight() {
      return menuStore.state.selectableAreaHeight + '%'
    },
    menuItems() {
      return menuStore.state.menuItems
    },
    difficulty() {
      return difficultyStore.state.difficulty
    },
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

.dash {
  background-color: #00d1b6;
  box-shadow: 0px 1px 3px 0.01px rgba(0, 209, 182, 0.7);
}

.dash-vertical {
  left: 50%;
  height: 5px;
  width: 1px;
}

.dash-horizontal {
  right: 0;
  top: 50%;
  height: 1px;
  width: 5px;
}
</style>