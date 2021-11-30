<template>
  <Window :title="'DISPONIBILITÉ INGRÉDIENTS'">
    <div class="d-flex flex-column align-items-center mx-4 h-100">
      <div class="d-flex flex-row justify-content-center w-100 align-items-center mb-4 mt-4" style="font-style: italic; font-size: 20px">
        <div>Plats du menu</div>
      </div>
      <div class="position-relative d-flex flex-row justify-content-center mb-5">
        <div
          v-for="(meal, index) in meals" :key="index"
          class="position-relative d-flex flex-row justify-content-center align-items-center"
          style="background: rgba(0, 209, 182, 0.6); width: 45px; height: 45px; margin: 0px 20px; font-size: 26px"
          @click="() => select(index)"
        >
          <div class="position-absolute" style="top: 5px">{{ meal.n }}</div>
        </div>

        <div
          class="position-absolute"
          style="border: 3px white solid; width: 61px; height: 80px; left: 12px; top: -16px; transition: left 1s ease-in-out"
          :style="{left: cursorLeft + 'px'}"
        >
          <div class="position-relative h-100">
            <div class="position-absolute" style="height: 38px; background: linear-gradient(white, rgba(0, 209, 182, 0.5)); width: 3px; bottom: -41px; left: 27px">
            </div>
          </div>
        </div>
      </div>
      <MealWidget :mealIndex="selectedMealIndex" class="mt-2 mb-5" style="flex-shrink: 1"/>
      <div class="position-relative w-100 h-100" style="flex-grow: 1">
        <InventoryWidget/>
      </div>
    </div>
  </Window>
</template>

<script>
import Window from '@/components/Window.vue'
import MealWidget from '@/components/MealWidget.vue'
import InventoryWidget from '@/components/InventoryWidget.vue'
import businessStore from '@/store/businessStore'

export default {
  name: "MenuWindow",
  components: {
    Window,
    MealWidget,
    InventoryWidget,
  },
  data() {
    return {
      selectedMealIndex: 1,
    }
  },
  computed: {
    meals() {
      return businessStore.state.meals
    },
    cursorLeft() {
      return this.selectedMealIndex * 85 + 12
    }
  },
  methods: {
    select(index) {
      this.selectedMealIndex = index
    }
  },
}
</script>