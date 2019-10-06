<template>
  <div class="position-relative">
    <div class="horizontal-wire selector-wire-1"></div>
    <div class="horizontal-wire selector-wire-2"></div>
    <div class="horizontal-wire selector-wire-3"></div>
    <div class="horizontal-wire selector-wire-4"></div>
    <div class="diagonal-wire menu-wire-1"></div>
    <div class="diagonal-wire menu-wire-2"></div>
    <div class="diagonal-wire menu-wire-3"></div>
    <div class="diagonal-wire menu-wire-4"></div>

    <div class="container-fluid">
      <div class="row">
        <div class="col-9">
          <MealSelectors/>
        </div>

        <div class="col-3">
          <MenuDisplay/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import MenuDisplay from '@/components/MenuDisplay.vue'
import MealSelectors from '@/components/MealSelectors.vue'

export default {
  name: 'MenuSelector',
  components: {
    MenuDisplay,
    MealSelectors,
  },
}
</script>

<style>
.meal-name-label {
  background: #006107;
  border-radius: 1px;
  padding: 1px 4px;
}

.horizontal-wire {
  position: absolute;
  height: 1px;
  /* total width - selector left margin - selector width - menu width - menu right margin */
  width: calc((1200px - 15px - 795px - 270px - 15px) / 2);
  left: calc(15px + 795px);
  border-top: 1px solid #00d1b6;
  box-shadow: 0px 1px 3px 0.01px rgba(0, 209, 182, 0.7);
}

.selector-wire-1 {
  top: calc(105.5px / 2);
}

.selector-wire-2 {
  top: calc(105.5px + 24px + 105.5px / 2);
}

.selector-wire-3 {
  top: calc((105.5px + 24px) * 2 + 105.5px / 2);
}

.selector-wire-4 {
  top: calc((105.5px + 24px) * 3 + 105.5px / 2);
}

.diagonal-wire {
  position: absolute;
  height: 1px;
  left: calc(15px + 795px + (1200px - 15px - 795px - 270px - 15px) / 2);
  border-top: 1px solid #00d1b6;
  box-shadow: 0px 1px 3px 0.01px rgba(0, 209, 182, 0.7);
}

.menu-wire-1 {
  top: calc(105.5px / 2);
  width: 75px;
  transform: translateY(26.5px) translateX(-11.5px) rotate(45deg);
}

.menu-wire-2 {
  top: calc(105.5px + 24px + 105.5px / 2);
  width: 57px;
  transform: translateY(9.5px) translateX(-2.5px) rotate(20deg);
}

.menu-wire-3 {
  top: calc((105.5px + 24px) * 2 + 105.5px / 2);
  width: 55px;
  transform: translateY(-4.5px) translateX(-1px) rotate(-10deg);
}

.menu-wire-4 {
  top: calc((105.5px + 24px) * 3 + 105.5px / 2);
  width: 69px;
  transform: translateY(-22px) translateX(-8px) rotate(-40deg);
}
</style>
