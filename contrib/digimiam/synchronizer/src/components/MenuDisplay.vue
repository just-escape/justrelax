<template>
  <div class="position-relative h-100">
    <!--<div class="connection-point display-display"></div>
    <div class="connection-point display-menu"></div>
    <div class="connection-point activate-activate"></div>
    <div class="connection-point activate-menu"></div>-->

    <div class="d-flex flex-column justify-content-between h-100">
      <div class="menu-container px-2 pb-1 text-center position-relative">
        <div class="menu-frame"></div>
        <div class="menu-background"></div>
        <div class="menu-title-ribbon mb-2 text-right p-2">DIGIMIAM MENU</div>
        <div class="date text-right mb-4">
            {{ date }}
        </div>
        <div
          v-for="(meal, mealIndex) in selectedMeals"
          :key="meal.id"
          class="ml-2"
          :class="{'mb-5': !isLastMeal(mealIndex), 'mb-3': isLastMeal(mealIndex)}"
        >
          <div class="meal-name text-left mb-1">
            {{ meal.name }}
            <sup v-if="meal.label" class="meal-name-label">
              {{ meal.label }}
            </sup>
          </div>
          <div class="d-flex flex-row justify-content-between meal-line">
            <span v-if="meal.configuredOnce === false" class="font-italic text-orange">
              ## Error ##
            </span>
            <span v-else class="font-italic">
              {{ dishes[meal.firstComponent][meal.secondComponent] }}
            </span>
            <span class="underline-dots flex-grow-1 mx-1">
            </span>
            <span class="price">
              <span v-if="meal.configuredOnce === false" class="text-orange">??</span>
              <span v-else>15</span>
              neoF
            </span>
          </div>
        </div>
      </div>

      <div class="d-flex flex-row justify-content-between mx-2 mb-3">
        <div class="position-relative">
          <div class="glowing-wire left-wire"></div>
          <div class="glowing-wire right-wire"></div>
          <ButtonDisplay></ButtonDisplay>
        </div>
        <div class="position-relative">
          <div class="glowing-wire left-wire"></div>
          <div class="glowing-wire right-wire"></div>
          <ButtonBlue>ACTIVATE</ButtonBlue>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ButtonBlue from '@/components/ButtonBlue.vue'
import ButtonDisplay from '@/components/ButtonDisplay.vue'
import MenuStore from '@/store/MenuStore.js'

export default {
  name: 'MenuDisplay',
  components: {
    ButtonBlue,
    ButtonDisplay,
  },
  computed: {
    date: function() {
      var date = new Date()
      date.setFullYear(2080)
      return this.$moment(date).format('LL')
    },
    selectedMeals: function() {
      return MenuStore.state.selectedMeals
    },
    isLastMeal: function() {
      return function(mealIndex) {
        return MenuStore.state.selectedMeals.length - 1 == mealIndex
      }
    },
    dishes: function() {
      return MenuStore.state.dishes
    },
  },
}
</script>

<style scoped>
.menu-container {
  border: 1px solid transparent;
  border-top: 9px solid transparent;
  padding-top: 38px;
}

.menu-background {
  background-color: rgba(00, 45, 64, 0.5);
  position: absolute;
  top: -9px;
  left: -1px;
  right: -1px;
  bottom: -1px;
  clip-path: polygon(
    100% 0%,
    100% 100%,
    0% 100%,
    0px calc(43px - 6px),
    43px 0px
  );
  z-index: -1;
}

.menu-frame {
  position: absolute;
  left: -1px;
  top: -9px;
  right: -1px;
  bottom: -1px;
  filter: drop-shadow(1px 1px 4px rgba(0, 209, 182, 0.75));
  clip-path: polygon(
    calc(100% - 1px) -10px,
    calc(100% + 10px) -10px,
    calc(100% + 10px) calc(100% + 10px),
    -10px calc(100% + 6px),
    -10px calc(43px - 6px - 6px),
    calc(43px + 3px - 6px) -10px,
    calc(100% - 1px) -10px,
    calc(100% - 1px) 9px,
    calc(43px + 1px) 9px,
    1px 43px,
    1px calc(100% - 1px),
    calc(100% - 1px) calc(100% - 1px)
  );
}

.menu-frame::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
  background-color: #00d1b6;
  clip-path: polygon(
    calc(100% - 1px) 0%,
    100% 0%,
    100% 100%,
    0% 100%,
    0% calc(43px - 6px),
    calc(43px + 3px) 0%,
    calc(100% - 1px) 0%,
    calc(100% - 1px) 9px,
    calc(43px + 1px) 9px,
    1px 43px,
    1px calc(100% - 1px),
    calc(100% - 1px) calc(100% - 1px)
  );
  z-index: 10;
}

.menu-title-ribbon {
  position: absolute;
  width: 100%;
  height: 34px;
  top: 0;
  right: 0;
  border-bottom: 1px solid #00d1b6;
  background-color: rgba(00, 45, 64, 0.6);
  font-size: 18px;
  clip-path: polygon(
    100% 0%,
    100% 100%,
    0% 100%,
    0px calc(43px - 9px),
    43px 0px
  );
  z-index: -1;
}

.date {
  font-size: 10px;
}

.meal-name {
  font-size: 18px;
}

.meal-name-label {
  font-size: 12px;
}

.meal-line {
  line-height: 1;
}

.underline-dots {
  border-bottom: 1px dotted #ffffff;
  margin-bottom: 3px;
}

.glowing-wire {
  position: absolute;
  /* meal module height - menu card height - button height - margin buttons/bottom */
  height: calc(510px - 439px - 36px - 16px);
  width: 1px;
  top: calc(-1 * (510px - 439px - 36px - 16px));
  border-left: 1px solid #00d1b6;
  box-shadow: 1px 0px 3px 0.01px rgba(0, 209, 182, 0.7);
}

.left-wire {
  left: 20%;
}

.right-wire {
  right: 20%;
}

.connection-point {
  position: absolute;
  height: 6px;
  width: 6px;
  background-color: #00d1b6;
  border-radius: 50%;
  z-index: 10;
}

.display-display {
  /* margin + button height - height / 2 (for centering) */
  bottom: calc(15px + 36px - 3px);
  left: 40px; /* random value */
}

.display-menu {
  bottom: 1px;
  left: 1px;
}

.activate-activate {
  /* margin + button height - height / 2 (for centering) */
  bottom: calc(15px + 36px - 3px);
  right: 45px; /* random value */
}

.activate-menu {
  bottom: 1px;
  right: 1px;
}
</style>
