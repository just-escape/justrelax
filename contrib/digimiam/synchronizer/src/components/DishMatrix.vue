<template>
  <div class="d-flex h-100 d-flex flex-column mx-3">
    <div class="selector-frame glowing-container position-relative w-100 h-100 mb-3">
      <div class="synthetic">Synthetic</div>
      <div class="organic">Organic</div>
      <div class="yummy-yummy">Yummy yummy</div>
      <div class="yummy">Yummy</div>

      <DishSelector
        v-for="(item, itemIndex) in menuItems"
        :key="item.id"
        :itemIndex="itemIndex"
      />

      <div
        v-for="area in selectableAreas" :key="area.id"
        class="selectable-area"
        :style="{top: area.top + '%', left: area.left + '%', height: selectableAreaHeight, width: selectableAreaWidth}">
      </div>
    </div>

    <div class="d-flex flex-row justify-content-center">
      <div class="button-like-frame generator-matrix-title">
        DISH GENERATOR MATRIX
      </div>
    </div>
  </div>
</template>

<script>
import DishSelector from '@/components/DishSelector.vue'
import MenuStore from '@/store/MenuStore.js'

export default {
  name: 'DishMatrix',
  components: {
    DishSelector,
  },
  computed: {
    selectableAreas: function() {
      return MenuStore.state.selectableAreas
    },
    selectableAreaWidth: function() {
      return MenuStore.state.selectableAreaWidth + '%'
    },
    selectableAreaHeight: function() {
      return MenuStore.state.selectableAreaHeight + '%'
    },
    menuItems: function() {
      return MenuStore.state.menuItems
    },
  },
}
</script>

<style scoped>
.synthetic {
  position: absolute;
  text-align: right;
  right: 0;
  bottom: calc(-14px - 5px);
  line-height: 1;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.65);
}

.organic {
  position: absolute;
  text-align: left;
  left: 0;
  bottom: calc(-14px - 5px);
  line-height: 1;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.65);
}

.yummy {
  position: absolute;
  bottom: 0;
  left: calc(-14px - 3px);
  writing-mode: tb-rl;
  transform: rotate(180deg);
  line-height: 1;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.65);
}

.yummy-yummy {
  position: absolute;
  top: 0;
  left: calc(-14px - 3px);
  writing-mode: tb-rl;
  transform: rotate(180deg);
  line-height: 1;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.65);
}

.selectable-area {
  position: absolute;
  /*border: 1px dotted rgba(255, 255, 255, 0.7);
  box-shadow: 0px 0px 14px -8px rgba(255, 255, 255, 1);*/
}

.selector-frame {
  height: 439px;
  width: 100%;
  background:
    linear-gradient(to right, transparent 20%, rgba(0, 150, 150, 0.09) 80%),
    linear-gradient(to top, transparent 20%, rgba(0, 150, 150, 0.09) 80%);
}

/* The same padding than on buttons */
.button-like-frame {
  padding: 0.375rem 0.75rem;
  height: 36px;
}

.generator-matrix-title {
  color: rgba(255, 255, 255, 0.65);
  background-color: rgba(00, 45, 80, 0.6);
  border: 1px solid rgba(0, 209, 182, 0.55);
}
</style>