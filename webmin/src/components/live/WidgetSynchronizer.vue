<template>
  <div>
    <div class="border-deepdark rounded p-3 mb-3">
        <div class="d-flex justify-content-between align-items-center">
            <div class="text-one-line-ellipsis min-width-100px mb-1">Notif maj menu holographique</div>
            <div
                v-if="getData('synchronizer_display_holographic_update_on_change') !== undefined"
                class="border mr-1 position-relative pointer"
                style="border-color: #ef8649 !important; height: 17px; width: 17px"
                @click="setData('synchronizer_display_holographic_update_on_change', !getData('synchronizer_display_holographic_update_on_change'))"
            >
                <i v-if="getData('synchronizer_display_holographic_update_on_change')" class="position-absolute text-jaffa fa fa-xs fa-fw fa-check" style="bottom: 0; right: 0"></i>
            </div>
        </div>
        <div class="d-flex justify-content-between align-items-center">
            <div class="text-one-line-ellipsis min-width-100px mb-1">Validation plats auto</div>
            <div
                v-if="getData('synchronizer_auto_validate_dishes') !== undefined"
                class="border mr-1 position-relative pointer"
                style="border-color: #ef8649 !important; height: 17px; width: 17px"
                @click="setData('synchronizer_auto_validate_dishes', !getData('synchronizer_auto_validate_dishes'))"
            >
                <i v-if="getData('synchronizer_auto_validate_dishes')" class="position-absolute text-jaffa fa fa-xs fa-fw fa-check" style="bottom: 0; right: 0"></i>
            </div>
        </div>
        <div class="d-flex justify-content-between align-items-center">
            <div class="text-one-line-ellipsis min-width-100px mb-1">Afficher le prix</div>
            <div
                v-if="getData('synchronizer_display_price') !== undefined"
                class="border mr-1 position-relative pointer"
                style="border-color: #ef8649 !important; height: 17px; width: 17px"
                @click="setData('synchronizer_display_price', !getData('synchronizer_display_price'))"
            >
                <i v-if="getData('synchronizer_display_price')" class="position-absolute text-jaffa fa fa-xs fa-fw fa-check" style="bottom: 0; right: 0"></i>
            </div>
        </div>
        <div class="d-flex justify-content-between align-items-center">
            <div class="text-one-line-ellipsis min-width-100px mb-1">Le prix compte</div>
            <div
                v-if="getData('synchronizer_price_matters') !== undefined"
                class="border mr-1 position-relative pointer"
                style="border-color: #ef8649 !important; height: 17px; width: 17px"
                @click="setData('synchronizer_price_matters', !getData('synchronizer_price_matters'))"
            >
                <i v-if="getData('synchronizer_price_matters')" class="position-absolute text-jaffa fa fa-xs fa-fw fa-check" style="bottom: 0; right: 0"></i>
            </div>
        </div>
        <div class="d-flex justify-content-between align-items-center">
            <div class="text-one-line-ellipsis min-width-100px mb-1">Instruction menu explicite</div>
            <div
                v-if="getData('synchronizer_display_menu_explicit_instruction') !== undefined"
                class="border mr-1 position-relative pointer"
                style="border-color: #ef8649 !important; height: 17px; width: 17px"
                @click="setData('synchronizer_display_menu_explicit_instruction', !getData('synchronizer_display_menu_explicit_instruction'))"
            >
                <i v-if="getData('synchronizer_display_menu_explicit_instruction')" class="position-absolute text-jaffa fa fa-xs fa-fw fa-check" style="bottom: 0; right: 0"></i>
            </div>
        </div>
    </div>
    <div class="border-deepdark rounded p-3 mb-3">
        <div class="d-flex justify-content-between align-items-center">
            <div class="text-one-line-ellipsis min-width-100px mb-1">Lumières mode strict</div>
            <div
                v-if="getData('synchronizer_strict_loading_mode') !== undefined"
                class="border mr-1 position-relative pointer"
                style="border-color: #ef8649 !important; height: 17px; width: 17px"
                @click="setData('synchronizer_strict_loading_mode', !getData('synchronizer_strict_loading_mode'))"
            >
                <i v-if="getData('synchronizer_strict_loading_mode')" class="position-absolute text-jaffa fa fa-xs fa-fw fa-check" style="bottom: 0; right: 0"></i>
            </div>
        </div>
        <div class="d-flex justify-content-between align-items-center">
            <div class="text-one-line-ellipsis min-width-100px mb-1">Instruction lumières explicites</div>
            <div
                v-if="getData('synchronizer_display_light_explicit_instruction') !== undefined"
                class="border mr-1 position-relative pointer"
                style="border-color: #ef8649 !important; height: 17px; width: 17px"
                @click="setData('synchronizer_display_light_explicit_instruction', !getData('synchronizer_display_light_explicit_instruction'))"
            >
                <i v-if="getData('synchronizer_display_light_explicit_instruction')" class="position-absolute text-jaffa fa fa-xs fa-fw fa-check" style="bottom: 0; right: 0"></i>
            </div>
        </div>
    </div>
  </div>
</template>

<script>
import roomStore from "@/store/roomStore.js"

export default {
  name: "WidgetSynchronizer",
  computed: {
    getData() {
      return (key) => { return roomStore.state.sessionData[this.roomId][key] }
    },
  },
  methods: {
    setData(key, value) {
      roomStore.dispatch('widgetAction', {
        channel: this.defaultChannel,
        widgetId: 'synchronizer',
        widgetType: 'synchronizer',
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