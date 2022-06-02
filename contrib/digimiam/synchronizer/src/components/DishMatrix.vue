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
            <span>{{ $t('Viande') }}</span>
          </div>
        </div>
        <div class="position-relative w-25 text-center">
          <div class="position-absolute dash dash-vertical"></div>
          <div class="mt-2">
            <i class="fa-fw fas fa-pizza-slice" style="opacity: 0.7"/>
            <span>{{ $t('Pizza') }}</span>
          </div>
        </div>
        <div class="position-relative w-25 text-center">
          <div class="position-absolute dash dash-vertical"></div>
          <div class="mt-2">
            <img src="@/assets/img/waffle.png" style="opacity: 0.7" height="16px"/>
            <span>{{ $t('Gaufre') }}</span>
          </div>
        </div>
        <div class="position-relative w-25 text-center">
          <div class="position-absolute dash dash-vertical"></div>
          <div class="mt-2">
            <img src="@/assets/img/jelly.svg" style="opacity: 0.7" height="16px"/>
            <span>{{ $t('Gelée') }}</span>
          </div>
        </div>
      </div>

      <div class="position-absolute d-flex flex-column h-100" style="left: -11px; width: 10px">
        <div class="position-relative h-25 d-flex">
          <div class="position-absolute dash dash-horizontal"></div>
          <div class="position-absolute h-100 d-flex justify-content-center" style="writing-mode: vertical-lr; transform: rotate(180deg); left: -20px">
            <i
              class="fa-fw fas fa-smile"
              style="opacity: 0.7; transform: rotate(90deg); margin-left: 3px"
            />
            <div style="margin-top: 2px">{{ $t('Portrait') }}</div>
          </div>
        </div>
        <div class="position-relative h-25 text-center">
          <div class="position-absolute dash dash-horizontal"></div>
          <div class="position-absolute h-100 d-flex justify-content-center" style="writing-mode: vertical-lr; transform: rotate(180deg); left: -20px">
            <i
              class="fa-fw fas fa-bug"
              style="opacity: 0.7; transform: rotate(90deg); margin-left: 3px"
            />
            <div style="margin-top: 2px">{{ $t('Insecte') }}</div>
          </div>
        </div>
        <div class="position-relative h-25 text-center">
          <div class="position-absolute dash dash-horizontal"></div>
          <div class="position-absolute h-100 d-flex justify-content-center" style="writing-mode: vertical-lr; transform: rotate(180deg); left: -20px">
            <i
              class="fa-fw fas fa-search"
              style="opacity: 0.7; transform: rotate(90deg); margin-left: 3px"
            />
            <div style="margin-top: 2px">{{ $t('Micro') }}</div>
          </div>
        </div>
        <div class="position-relative h-25 text-center">
          <div class="position-absolute dash dash-horizontal"></div>
          <div class="position-absolute h-100 d-flex justify-content-center" style="writing-mode: vertical-lr; transform: rotate(180deg); left: -20px">
            <img
              src="@/assets/img/seaweed.png" height="16px"
              style="opacity: 0.7; transform: rotate(90deg)"
            />
            <div class="mt-2">{{ $t('Algue') }}</div>
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

    <div
      class="d-flex flex-row"
      :class="{'justify-content-around': !autoValidateDishes, 'justify-content-center': autoValidateDishes}"
      style="margin-top: 15px"
    >
      <div class="button-like-frame generator-matrix-title position-relative">
        {{ $t('dish_generator_matrix') }}
      </div>
      <div :class="{'d-none': autoValidateDishes}" style="width: 33%">
        <ButtonValidate @click="validate" class="btn-block" :disabled="success || autoValidateDishes"/>
      </div>
    </div>
  </div>
</template>

<script>
import ButtonValidate from '@/components/ButtonValidate.vue'
import DishSelectorCursor from '@/components/DishSelectorCursor.vue'
import menuStore from '@/store/menuStore.js'
import difficultyStore from '@/store/difficultyStore.js'

export default {
  name: 'DishMatrix',
  components: {
    ButtonValidate,
    DishSelectorCursor,
  },
  data() {
    return {
      lockButton: false,
    }
  },
  computed: {
    autoValidateDishes: function() {
      return menuStore.state.autoValidateDishes
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
    success() {
      return menuStore.state.success
    },
  },
  methods: {
    validate() {
      if (menuStore.state.success || menuStore.state.validating || this.lockButton) {
        return
      }
      this.lockButton = true

      menuStore.commit("lockValidate")
      setTimeout(this.validatePostAnimation, 1550)
    },
    validatePostAnimation() {
      this.lockButton = false
      menuStore.commit("unlockValidate")
      menuStore.commit("validateMenu", menuStore.getters)
    },
  }
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

.glowing-wire {
  position: absolute;
  height: 24px;
  width: 1px;
  bottom: 40px;
  border-left: 1px solid #00d1b6;
  box-shadow: 1px 0px 3px 0.01px rgba(0, 209, 182, 0.7);
}

.left-wire {
  left: 20%;
}

.right-wire {
  right: 20%;
}
</style>