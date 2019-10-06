<template>
  <div class="container-fluid px-0">
    <div class="row">
      <div
        v-for="(meal, mealIndex) in selectedMeals"
        :key="meal.id"
        class="col-11"
        :class="{'mb-4': !isLastMeal(mealIndex), 'mb-3': isLastMeal(mealIndex)}"
      >
        <div
          class="glowing-container meal-selector-container position-relative p-3"
          style="height: 105.5px"
        >
          <div class="position-absolute m-3" style="color: red; transform: translateX(300px) translateY(40px) rotate(-5deg)">Configurer correctement les sliders</div>

          <div class="d-flex flex-row justify-content-between h-100">
            <div class="d-flex flex-column justify-content-around">
              <div>
                {{ meal.name }}
                <sup v-if="meal.label" class="meal-name-label">
                  {{ meal.label }}
                </sup>
              </div>
              <div>
              <ButtonDisplay/>
              </div>
            </div>

            <div class="row">
              <div class="position-relative mt-4" style="width: 180px">
                <MealSelector :mealComponent="'firstComponent'" :mealIndex="mealIndex"/>
              </div>
              <div class="position-relative mt-4" style="width: 180px">
                <MealSelector :mealComponent="'secondComponent'" :mealIndex="mealIndex"/>
              </div>
              <div class="position-relative mt-4" style="width: 180px">
                <input type="range">
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ButtonDisplay from '@/components/ButtonDisplay.vue'
import MealSelector from '@/components/MealSelector.vue'
import MenuStore from '@/store/MenuStore.js'

export default {
  name: 'MealSelectors',
  components: {
    MealSelector,
    ButtonDisplay,
  },
  computed: {
    selectedMeals: function() {
      return MenuStore.state.selectedMeals
    },
    isLastMeal: function() {
      return function(mealIndex) {
        return MenuStore.state.selectedMeals.length - 1 == mealIndex
      }
    },
  },
}
</script>

<style scoped>
.meal-selector-container div {
  line-height: 1;
}
</style>
