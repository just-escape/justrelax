<template>
  <div class="window d-flex flex-column" :class="{hide: !displayed}">
    <div class="d-flex flex-row rounded-top bg-info shadow-box-top align-items-center h-header">
      <Neons class="ml-2" color="var(--light)"/>
      <h3 class="size-12 py-1 mx-3 mb-0 text-white">ERROR</h3>
      <Neons class="mr-2" color="var(--light)"/>
    </div>
    <div class="border-left-bottom-right shadow-box-top bg-light-transparent p-3">
      <div class="media">
        <div class="mr-3 bg-info glow align-self-center d-flex justify-content-center align-items-center" style="width: 50px; height: 50px; border-radius: 50%">
          <i class="fas fa-info" style="color: var(--light);font-size: 1.7rem;"></i>
        </div>
        <div class="media-body">
          Erreur ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore.
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Neons from "@/components/Neons.vue"

export default {
  name: "WarningWindow",
  components: {
    Neons,
  },
  props: {
    displayed: Boolean,
  }
}
</script>

<style scoped>
.window {
  transition: transform 0.7s ease-in-out, left 0.4s ease-in-out, bottom 0.4s ease-in-out;
  width: 90%;
  left: 5%;
  bottom: 400px;
}

.hide {
  left: calc(5% + 200px) !important;
  bottom: calc(400px - 300px);
  transform: scale(0);
}

.h-header {
  height: 40px;
}

.bg-light-transparent {
  background: rgba(248, 249, 250, 0.65);
}

.border-left-bottom-right {
  border: 3px solid var(--info);
  border-top: 0px;
  border-bottom-left-radius: 0.25rem;
  border-bottom-right-radius: 0.25rem;
}

.glow {
  box-shadow: 0px 0px 4px var(--info);
}

.shadow-box-top {
  box-shadow: 1px -1px 5px var(--info);
}
</style>
