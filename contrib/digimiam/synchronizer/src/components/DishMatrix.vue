<template>
  <div class="d-flex h-100 d-flex flex-column mx-3">
    <div class="selector-frame glowing-container position-relative w-100 h-100 mb-4">

      <DishSelectorCursor
        v-for="(item, itemIndex) in menuItems"
        :key="item.id"
        :itemIndex="itemIndex"
      />

      <div class="position-absolute d-flex flex-row w-100" style="top: calc(100% + 1px)">
        <div class="position-relative w-25 text-center">
          <div class="position-absolute dash dash-vertical"></div>
          <div class="mt-2">
            <i class="fa-fw fas fa-drumstick-bite" style="opacity: 0.7"/>
            <span>Viande</span>
          </div>
        </div>
        <div class="position-relative w-25 text-center">
          <div class="position-absolute dash dash-vertical"></div>
          <div class="mt-2">
            <i class="fa-fw fas fa-pizza-slice" style="opacity: 0.7"/>
            <span>Pizza</span>
          </div>
        </div>
        <div class="position-relative w-25 text-center">
          <div class="position-absolute dash dash-vertical"></div>
          <div class="mt-2">
            <img src="@/assets/img/waffle.png" style="opacity: 0.7" height="16px"/>
            <span>Gaufre</span>
          </div>
        </div>
        <div class="position-relative w-25 text-center">
          <div class="position-absolute dash dash-vertical"></div>
          <div class="mt-2">
            <img src="@/assets/img/jelly.svg" style="opacity: 0.7" height="16px"/>
            <span>Gelée</span>
          </div>
        </div>
      </div>

      <div class="position-absolute d-flex flex-column h-100" style="left: -11px; width: 10px">
        <div class="position-relative h-25 d-flex">
          <div class="position-absolute dash dash-horizontal"></div>
          <div class="position-absolute h-100 d-flex justify-content-center" style="writing-mode: vertical-lr; transform: rotate(180deg); left: -20px">
            <i
              class="fa-fw fas fa-smile"
              style="opacity: 0.7; transform: rotate(90deg)"
            />
            <div>Portrait</div>
          </div>
        </div>
        <div class="position-relative h-25 text-center">
          <div class="position-absolute dash dash-horizontal"></div>
          <div class="position-absolute h-100 d-flex justify-content-center" style="writing-mode: vertical-lr; transform: rotate(180deg); left: -20px">
            <i
              class="fa-fw fas fa-bug"
              style="opacity: 0.7; transform: rotate(90deg)"
            />
            <div>Insecte</div>
          </div>
        </div>
        <div class="position-relative h-25 text-center">
          <div class="position-absolute dash dash-horizontal"></div>
          <div class="position-absolute h-100 d-flex justify-content-center" style="writing-mode: vertical-lr; transform: rotate(180deg); left: -20px">
            <i
              class="fa-fw fas fa-search"
              style="opacity: 0.7; transform: rotate(90deg)"
            />
            <div>Micro-</div>
          </div>
        </div>
        <div class="position-relative h-25 text-center">
          <div class="position-absolute dash dash-horizontal"></div>
          <div class="position-absolute h-100 d-flex justify-content-center" style="writing-mode: vertical-lr; transform: rotate(180deg); left: -20px">
            <img
              src="@/assets/img/seaweed.png" height="16px"
              style="opacity: 0.7; rotate(90deg)"
            />
            <div>Algue</div>
          </div>
        </div>
      </div>

      <div
        v-for="area in selectableAreas" :key="area.id"
        class="selectable-area"
        :style="{
          top: area.top + '%',
          left: area.left + '%',
          height: selectableAreaHeight,
          width: selectableAreaWidth,
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
import DishSelectorCursor from '@/components/DishSelectorCursor.vue'
import menuStore from '@/store/menuStore.js'
import difficultyStore from '@/store/difficultyStore.js'

export default {
  name: 'DishMatrix',
  components: {
    DishSelectorCursor,
  },
  computed: {
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