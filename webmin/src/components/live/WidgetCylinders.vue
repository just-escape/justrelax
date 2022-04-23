<template>
    <div class="border-deepdark rounded p-3 mb-3">
        <div class="d-flex flex-row justify-content-end mb-2">
            <ButtonJaffa size="sm" @click="reset">
                <i class="fa fa-fw fa-undo-alt"></i>
            </ButtonJaffa>
        </div>
        <div class="d-flex justify-content-between align-items-center">
            <div class="text-one-line-ellipsis min-width-100px mb-1">Mode jouable ?</div>
            <div
                v-if="getData('cylinders_playing') !== undefined"
                class="border mr-1 position-relative pointer"
                style="border-color: #ef8649 !important; height: 17px; width: 17px"
                @click="setData('cylinders_playing', !getData('cylinders_playing'))"
            >
                <i v-if="getData('cylinders_playing')" class="position-absolute text-jaffa fa fa-xs fa-fw fa-check" style="bottom: 0; right: 0"></i>
            </div>
        </div>
        <div class="d-flex justify-content-between align-items-center">
            <div class="text-one-line-ellipsis min-width-100px mb-1">Montrer les erreurs</div>
            <div
                v-if="getData('cylinders_reveal_mistakes') !== undefined"
                class="border mr-1 position-relative pointer"
                style="border-color: #ef8649 !important; height: 17px; width: 17px"
                @click="setData('cylinders_reveal_mistakes', !getData('cylinders_reveal_mistakes'))"
            >
                <i v-if="getData('cylinders_reveal_mistakes')" class="position-absolute text-jaffa fa fa-xs fa-fw fa-check" style="bottom: 0; right: 0"></i>
            </div>
        </div>
        <div class="d-flex justify-content-between align-items-center">
            <div class="text-one-line-ellipsis min-width-100px mb-1">Succès</div>
            <div
                v-if="getData('cylinders_success') !== undefined"
                class="border mr-1 position-relative" :class="{pointer: !getData('cylinders_success')}"
                style="border-color: #ef8649 !important; height: 17px; width: 17px"
                @click="setData('cylinders_success', !getData('cylinders_success'))"
            >
                <i v-if="getData('cylinders_success')" class="position-absolute text-jaffa fa fa-xs fa-fw fa-check" style="bottom: 0; right: 0"></i>
            </div>
        </div>
    </div>
</template>

<script>
import ButtonJaffa from "@/components/common/ButtonJaffa.vue"
import roomStore from "@/store/roomStore.js"

export default {
  name: "WidgetCylinders",
  components: {
    ButtonJaffa,
  },
  computed: {
    getData() {
      return (key) => { return roomStore.state.sessionData[this.roomId][key] }
    },
  },
  methods: {
    reset() {
      roomStore.dispatch(
        'widgetAction',
        {
          channel: this.defaultChannel,
          widgetId: 'cylinders',
          widgetType: 'cylinders',
          action: "reset",
        }
      )
    },
    setData(key, value) {
      roomStore.dispatch('widgetAction', {
        channel: this.defaultChannel,
        widgetId: 'cylinders',
        widgetType: 'cylinders',
        action: 'set',
        key: key,
        value: value,
      })
    },
  },
  props: [
    "defaultChannel",
    "row",
    "roomId",
  ]
}
</script>