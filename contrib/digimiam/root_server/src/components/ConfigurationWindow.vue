<template>
  <Window :title="$t('configuration')" class="h-100">
    <div class="d-flex h-100">
      <div class="d-flex flex-column lh-1 mx-4 justify-content-center h-100 w-100">
        <div class="d-flex flex-row mb-4 justify-content-between align-items-center">
            <div>{{ $t('mode') }}</div>
            <OnOffSwitch :editable="false" :initiallyOn="false" :width="124" :onText="$t('marmitron')" :offText="$t('manual')"/>
        </div>
        <div class="d-flex flex-row mb-2 justify-content-between align-items-center">
            <div>{{ $t('security') }}</div>
            <OnOffSwitch :editable="false" :initiallyOn="true"/>
        </div>
        <div class="d-flex flex-row mb-2 justify-content-between align-items-center">
            <div>{{ $t('ongoing_maintenance') }}</div>
            <OnOffSwitch :editable="false" :initiallyOn="true" :onText="$t('yes')" :offText="$t('no')"/>
        </div>
        <div class="d-flex flex-row mb-4 justify-content-between align-items-center">
            <div>{{ $t('open') }}</div>
            <OnOffSwitch :editable="false" :initiallyOn="false" :onText="$t('yes')" :offText="$t('no')"/>
        </div>
        <div class="d-flex flex-row mb-2 justify-content-between align-items-center">
            <div>{{ $t('supply') }}</div>
            <OnOffSwitch :initiallyOn="true" :width="124" :onText="$t('marmitron')" :offText="$t('manual')"/>
        </div>
        <div class="d-flex flex-row mb-2 justify-content-between align-items-center">
            <div>{{ $t('food_hydroinflation') }}</div>
            <OnOffSwitch :initiallyOn="true" :onText="$t('yes')" :offText="$t('no')"/>
        </div>
        <div class="d-flex flex-row justify-content-between align-items-center">
            <div>{{ $t('air_quality') }}</div>
            <OnOffSwitch :initiallyOn="false" :width="131" :onText="$t('optimal')" :offText="$t('economic')"/>
        </div>
      </div>
    </div>
  </Window>
</template>

<script>
import Window from '@/components/Window.vue'
import OnOffSwitch from '@/components/OnOffSwitch.vue'

export default {
  name: "ConfigurationWindow",
  components: {
    Window,
    OnOffSwitch,
  }
}
</script>

<style scoped>
.underline-dots {
  font-size: 18px;
  border-bottom: 1px dotted #ffffff;
  margin-bottom: 3px;
}

.opacity-25 {
  opacity: 0.25;
}
</style>