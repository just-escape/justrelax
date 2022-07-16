<template>
  <div class="d-flex h-100 d-flex flex-column mx-3">
    <div class="selector-frame glowing-container position-relative w-100 h-100 mb-4">

      <div
        v-for="(row, rowIndex) in rows"
        :key="'row-' + rowIndex"
        class="position-absolute w-100"
        :class="{'row-animated-background': animatedRowIndex == rowIndex}"
        style="left: 0%; background: rgba(0, 209, 182); opacity: 0"
        :style="{'height': selectableAreaHeight, 'top': row.top}"
      >{{row.animationCount}}</div>

      <div
        v-for="(column, columnIndex) in columns"
        :key="'col-' + columnIndex"
        class="position-absolute h-100"
        :class="{'column-animated-background': animatedColumnIndex == columnIndex}"
        style="top: 0px; background: rgba(0, 209, 182); opacity: 0"
        :style="{'width': selectableAreaWidth, 'left': column.left}"
      >{{column.animationCount}}</div>

      <DishSelectorCursor
        v-for="(item, itemIndex) in menuItems"
        :key="item.id"
        :itemIndex="itemIndex"
      />

      <div class="position-absolute d-flex flex-row w-100" style="top: calc(100% + 1px)">
        <div class="position-relative w-25 text-center">
          <div class="position-absolute dash dash-vertical"></div>
          <div class="mt-2" :class="{'label-animated-scale': columnLabelScale == 'Viande'}">
            <i class="fa-fw fas fa-drumstick-bite" style="opacity: 0.7"/>
            <span>{{ $t('Viande') }}</span>
          </div>
        </div>
        <div class="position-relative w-25 text-center">
          <div class="position-absolute dash dash-vertical"></div>
          <div class="mt-2" :class="{'label-animated-scale': columnLabelScale == 'Pizza'}">
            <i class="fa-fw fas fa-pizza-slice" style="opacity: 0.7"/>
            <span>{{ $t('Pizza') }}</span>
          </div>
        </div>
        <div class="position-relative w-25 text-center">
          <div class="position-absolute dash dash-vertical"></div>
          <div class="mt-2" :class="{'label-animated-scale': columnLabelScale == 'Gaufre'}">
            <img src="@/assets/img/waffle.png" style="opacity: 0.7" height="16px"/>
            <span>{{ $t('Gaufre') }}</span>
          </div>
        </div>
        <div class="position-relative w-25 text-center">
          <div class="position-absolute dash dash-vertical"></div>
          <div class="mt-2" :class="{'label-animated-scale': columnLabelScale == 'Gelée'}">
            <img src="@/assets/img/jelly.svg" style="opacity: 0.7" height="16px"/>
            <span>{{ $t('Gelée') }}</span>
          </div>
        </div>
      </div>

      <div class="position-absolute d-flex flex-column h-100" style="left: -11px; width: 10px">
        <div class="position-relative h-25 d-flex">
          <div class="position-absolute dash dash-horizontal"></div>
          <div
            class="position-absolute h-100 d-flex justify-content-center"
            style="writing-mode: vertical-lr; transform: rotate(180deg); left: -20px"
            :class="{'label-animated-scale-180': rowLabelScale == 'Portrait'}"
          >
            <i
              class="fa-fw fas fa-smile"
              style="opacity: 0.7; transform: rotate(90deg); margin-left: 3px"
            />
            <div style="margin-top: 2px">{{ $t('Portrait') }}</div>
          </div>
        </div>
        <div class="position-relative h-25 text-center">
          <div class="position-absolute dash dash-horizontal"></div>
          <div
            class="position-absolute h-100 d-flex justify-content-center"
            style="writing-mode: vertical-lr; transform: rotate(180deg); left: -20px"
            :class="{'label-animated-scale-180': rowLabelScale == 'Insecte'}"
          >
            <i
              class="fa-fw fas fa-bug"
              style="opacity: 0.7; transform: rotate(90deg); margin-left: 3px"
            />
            <div style="margin-top: 2px">{{ $t('Insecte') }}</div>
          </div>
        </div>
        <div class="position-relative h-25 text-center">
          <div class="position-absolute dash dash-horizontal"></div>
          <div
            class="position-absolute h-100 d-flex justify-content-center"
            style="writing-mode: vertical-lr; transform: rotate(180deg); left: -20px"
            :class="{'label-animated-scale-180': rowLabelScale == 'Micro'}"
          >
            <i
              class="fa-fw fas fa-search"
              style="opacity: 0.7; transform: rotate(90deg); margin-left: 3px"
            />
            <div style="margin-top: 2px">{{ $t('Micro') }}</div>
          </div>
        </div>
        <div class="position-relative h-25 text-center">
          <div class="position-absolute dash dash-horizontal"></div>
          <div
            class="position-absolute h-100 d-flex justify-content-center"
            style="writing-mode: vertical-lr; transform: rotate(180deg); left: -20px"
            :class="{'label-animated-scale-180': rowLabelScale == 'Algue'}"
          >
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

      <div
        class="z-index-20 position-absolute"
        style="width: 540px; height: 360px"
        :style="{top: windowTop, left: windowLeft, transform: windowTransform}"
      >
        <Window :title="$t('INFORMATION SUR LE MENU HOLOGRAPHIQUE')" class="text-light text-code-new-roman">
          <div class="d-flex flex-column h-100 justify-content-center align-items-center bg-black-transparent">
            <div class="d-flex flex-column align-items-center h-100 justify-content-around px-4">
              <div class="text-center">
                <div class="mb-3" style="font-size: 24px; color: #00d1b6">
                  {{ $t(lastSelectedRowLabel) }} + {{ $t(lastSelectedColumnLabel) }} = {{ $t(lastSelectedDish) }}
                </div>
                <div style="font-size: 18px">
                  {{ $t('Le menu holographique affiche maintenant ') + $t(lastSelectedDishPronoun) +
                     $t(' sur le Plat ') + lastSelectedDishIndex + $t('. Le Plat ') +
                     lastSelectedDishIndex + $t(' coûte ') + lastSelectedPrice + '&nbsp;nF.' }}
                </div>
              </div>
              <div style="font-size: 40px">
                <div>
                  <ButtonBlue @click="ackWindow" class="px-5">{{ $t('Ok') }}</ButtonBlue>
                </div>
              </div>
            </div>
          </div>
        </Window>
      </div>
    </div>
  </div>
</template>

<script>
import ButtonValidate from '@/components/ButtonValidate.vue'
import DishSelectorCursor from '@/components/DishSelectorCursor.vue'
import ButtonBlue from '@/components/ButtonBlue.vue'
import menuStore from '@/store/menuStore.js'
import difficultyStore from '@/store/difficultyStore.js'
import Window from '@/components/Window.vue'

export default {
  name: 'DishMatrix',
  components: {
    ButtonValidate,
    DishSelectorCursor,
    Window,
    ButtonBlue,
  },
  data() {
    return {
      windowTopOffset: 10,
      windowLeftOffset: 250,
      windowScaleX: 0,
      windowScaleY: 0,
      lockButton: false,
      rowLabelScale: null,
      animatedRowIndex: null,
      rows: [
        {
          top: '8%',
        },
        {
          top: '31%',
        },
        {
          top: '54%',
        },
        {
          top: '77%',
        },
      ],
      columnLabelScale: null,
      animatedColumnIndex: null,
      columns: [
        {
          left: '8%',
        },
        {
          left: '31%',
        },
        {
          left: '54%',
        },
        {
          left: '77%',
        },
      ],
      windowDisplayed: false,
      lastSelectedPrice: null,
      lastSelectedRowLabel: null,
      lastSelectedColumnLabel: null,
      lastSelectedDish: null,
      lastSelectedDishPronoun: null,
      lastSelectedDishIndex: null,
    }
  },
  computed: {
    windowTop() {
      return "calc(0px + " + this.windowTopOffset + "px)"
    },
    windowLeft() {
      return "calc(0px + " + this.windowLeftOffset + "px)"
    },
    windowTransform() {
      return "scaleX(" + this.windowScaleX + ") scaleY(" + this.windowScaleY + ")"
    },
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
    onMenuChangedSignal() {
      return menuStore.state.onMenuChangedSignal
    },
    lastChangedItemIndex() {
      return menuStore.state.lastChangedItemIndex
    },
    dishesComposition() {
      return menuStore.state.dishesComposition
    },
    explainOnDishChangedCounter() {
      return menuStore.state.explainOnDishChangedCounter
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
    setAnimatedValuesOnMenuChange(rowIndex, columnIndex, rowLabel, columnLabel) {
      this.animatedRowIndex = rowIndex
      this.animatedColumnIndex = columnIndex
      this.rowLabelScale = rowLabel
      this.columnLabelScale = columnLabel
    },
    ackWindow() {
      this.windowDisplayed = false
    },
  },
  watch: {
    onMenuChangedSignal() {
      let lastChangedDish = this.menuItems[this.lastChangedItemIndex].dish
      if (lastChangedDish === null) {
        return
      }

      this.lastSelectedDishIndex = this.menuItems[this.lastChangedItemIndex].id
      this.lastSelectedPrice = this.menuItems[this.lastChangedItemIndex].price
      this.lastSelectedDish = this.menuItems[this.lastChangedItemIndex].dish
      this.lastSelectedRowLabel = this.dishesComposition[lastChangedDish].rowLabel
      this.lastSelectedColumnLabel = this.dishesComposition[lastChangedDish].columnLabel
      this.lastSelectedDishPronoun = this.dishesComposition[lastChangedDish].pronoun

      this.setAnimatedValuesOnMenuChange(null, null, null, null)
      setTimeout(
        this.setAnimatedValuesOnMenuChange, 10,
        this.dishesComposition[lastChangedDish].rowIndex, this.dishesComposition[lastChangedDish].columnIndex,
        this.dishesComposition[lastChangedDish].rowLabel, this.dishesComposition[lastChangedDish].columnLabel,
      )

      if (this.explainOnDishChangedCounter > 0) {
        this.windowDisplayed = true
        menuStore.commit("setExplainOnDishChangedCounter", this.explainOnDishChangedCounter - 1)
      }
    },
    windowDisplayed(newValue) {
      if (newValue) {
        this.$anime({
          targets: this,
          windowScaleX: 1,
          windowScaleY: 1,
          duration: 400,
          easing: 'easeInQuad',
        })
      } else {
        this.$anime({
          targets: this,
          windowScaleX: 0,
          windowScaleY: 0,
          duration: 700,
          easing: 'easeInOutQuad',
        })
      }
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

.row-animated-background {
  animation: row_animate 2s linear 1;
}

@keyframes row_animate {
  0% {
    opacity: 0;
  }
  50% {
    opacity: 0.5;
  }
  100% {
    opacity: 0;
  }
}

.column-animated-background {
  animation: column_animate 2s linear 1;
}

@keyframes column_animate {
  0% {
    opacity: 0;
  }
  50% {
    opacity: 0.5;
  }
  100% {
    opacity: 0;
  }
}

.label-animated-scale {
  animation: scale 0.8s linear 1;
}

@keyframes scale {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.8);
  }
  100% {
    transform: scale(1);
  }
}

.label-animated-scale-180 {
  animation: scale_180 0.8s linear 1;
}

@keyframes scale_180 {
  0% {
    transform: rotate(180deg) scale(1);
  }
  50% {
    transform: rotate(180deg) scale(1.8);
  }
  100% {
    transform: rotate(180deg) scale(1);
  }
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