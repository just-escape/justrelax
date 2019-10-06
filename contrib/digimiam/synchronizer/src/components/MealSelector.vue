<template>
  <div class="d-flex justify-content-center">
    <div class="vgraduation vg-0"></div>
    <div class="vgraduation vg-33"></div>
    <div class="vgraduation vg-66"></div>
    <div class="vgraduation vg-100"></div>
    <div class="graduation-bar"></div>

    <div class="graduation-label gl-0">Label 0</div>
    <div class="graduation-label gl-33">Label 33</div>
    <div class="graduation-label gl-66">Label 66</div>
    <div class="graduation-label gl-100">Label 100</div>

    <input
      type="range" min="0" max="3"
      v-model="meal[mealComponent]"
      @change="onMealSelectorChange(mealIndex)"
    >
  </div>
</template>

<script>
import MenuStore from '@/store/MenuStore.js'

export default {
  name: 'MealSelector',
  computed: {
    meal: function() {
      return MenuStore.state.selectedMeals[this.mealIndex]
    },
  },
  methods: {
    onMealSelectorChange: function(mealIndex) {
      MenuStore.commit('onMealSelectionChange', mealIndex)
    },
  },
  props: ['mealComponent', 'mealIndex']
}
</script>

<style scoped>
input[type=range] {
  /* Hides the slider so that custom slider can be made */
  -webkit-appearance: none;
  /* Otherwise white in Chrome */
  background: transparent;
}

input[type=range]::-webkit-slider-thumb {
  -webkit-appearance: none;
  height: 20px;
  width: 10px;
  border-radius: 3px;
  background: #00d1b6;
  cursor: pointer;
  box-shadow: 0px 0px 14px -6px rgba(0, 209, 182, 1);
  z-index: 2;
}

input[type=range]:focus {
  /* Removes the blue border. */
  outline: none;
}

input[type=range]::-webkit-slider-runnable-track {
  /* You need to specify a margin in Chrome, but in Firefox and IE it is automatic */
  margin-top: 7px;
  height: 20px;
  cursor: pointer;
}

.graduations {
  position: absolute;
}

.vgraduation {
  position: absolute;
  top: 10px;
  height: 14px;
  border-left: 2px solid #00d1b6;
  border-radius: 1px;
  z-index: 0;
}

.vg-0 {
  left: calc(15px + 4px); /* bootstrap col margin + cursor center */
}

.vg-33 {
  left: calc(15px + 50px); /* bootstrap col margin + 33% offset */
}

.vg-66 {
  right: calc(15px + 50px); /* bootstrap col margin + 33% offset */
}

.vg-100 {
  right: calc(15px + 4px); /* bootstrap col margin + cursor center */
}

.graduation-bar {
  position: absolute;
  left: calc(15px + 4px); /* bootstrap col margin + cursor center */
  top: 16px;
  width: calc(100% - 2 * 15px - 2 * 4px); /* bootstrap col margin - cursor center */
  border-top: 2px solid rgba(0, 209, 182, 0.4);
  border-radius: 1px;
  z-index: 0;
}

.graduation-label {
  position: absolute;
  font-size: 10px;
  transform: rotate(-45deg);
  top: -19px;
  white-space: nowrap;
}

/* manual tuning */
.gl-0 {
  left: 4px;
  top: -17px;
}

.gl-33 {
  left: 50px;
}

.gl-66 {
  left: 100px;
}

.gl-100 {
  left: 146px;
  top: -21px; /* I don't understand why */
}
</style>
