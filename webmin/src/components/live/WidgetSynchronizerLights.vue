<template>
  <div class="d-flex justify-content-between align-items-center">
    <div class="text-one-line-ellipsis min-width-100px">{{ row.name }}</div>

    <div class="d-flex flex-row">
      <div
        v-for="(isDeativated, color) in deactivatedColors"
        :key="color"
        @click="click(color)"
        style="width: 20px; height: 20px; border: 2px solid grey; border-radius: 50%"
        :style="{background: isDeativated ? 'transparent' : colorNameToRgb[color], 'border-color': colorNameToRgb[color]}"
        class="mr-1-not-last"
      >
      </div>
    </div>
  </div>
</template>

<script>
import roomStore from "@/store/roomStore.js"

export default {
  name: "WidgetSynchronizerLights",
  data() {
    return {
      colorNameToRgb: {
        white: 'rgb(255, 255, 255)',
        orange: 'rgb(253, 126, 20)',
        blue: 'rgb(0, 170, 255)',
        green: 'rgb(40, 167, 69)',
        red: 'rgb(220, 53, 69)',
        pink: 'rgb(232, 62, 140)',
      }
    }
  },
  computed: {
    deactivatedColors() {
      return roomStore.state.sessionData[this.roomId].synchronizer_disabled_colors || {}
    }
  },
  methods: {
    click(color) {
      roomStore.dispatch('widgetAction', {
        channel: this.defaultChannel,
        widgetId: 'synchronizer_lights',
        widgetType: 'synchronizer_lights',
        action: 'set_disabled',
        color: color,
        disabled: !roomStore.state.sessionData[this.roomId].synchronizer_disabled_colors[color],
      })
    }
  },
  props: [
    "defaultChannel",
    "row",
    "roomId",
  ]
}
</script>

<style scoped>
.mr-1-not-last:not(:last-child) {
  margin-right: 0.25rem;
}
</style>