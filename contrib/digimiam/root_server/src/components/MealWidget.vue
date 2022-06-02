<template>
  <div class="glowing-container w-100 mb-4 p-3">
    <div class="d-flex flex-row justify-content-center mb-4" style="font-size: 20px">{{label}}</div>
    <div class="d-flex flex-row justify-content-between mb-2">
      <div style="font-style: italic">{{ $t('Prix') }}</div>
      <div>{{price}} {{ $t('NéoFrancs') }}</div>
    </div>
    <div class="d-flex flex-row justify-content-between mb-2">
      <div style="font-style: italic">{{ $t('Marge financière') }}</div>
      <div>{{margin}} {{ $t('NéoFrancs') }}</div>
    </div>
    <div class="d-flex flex-row justify-content-between mb-2">
      <div style="font-style: italic">{{ $t('Temps de production') }}</div>
      <div>{{cycles}} {{ $t('cycles') }}</div>
    </div>
    <div class="d-flex flex-row justify-content-between mb-2">
      <div v-if="!simplifiedUI" style="font-style: italic" class="transition-1s">{{ $t('Qualité de production') }}</div>
      <div v-if="!simplifiedUI" class="transition-1s"><input ref="qualityInput" type="range" min="0" max="100"></div>
    </div>
    <div class="d-flex justify-content-between align-items-center mb-2 w-100 transition-1s" :class="{'flex-column': simplifiedUI}">
      <div class="transition-1s" :class="{'mb-2': simplifiedUI}" style="font-style: italic">{{ $t('Disponibilité ingrédients') }}</div>
      <div class="transition-1s position-relative" :class="{'w-100': simplifiedUI}">
        <div
          :style="{height: simplifiedUI ? '50px' : '32px', width: simplifiedUI ? '100%' : '100px'}"
          class="transition-1s d-flex align-items-center justify-content-center"
        >
          <div :class="{pulsate: pulsate}" class="transition-1s"></div>
          <div v-if="availabilityLoading" class="loading"></div>
          <ButtonBlue v-else
            @click="click"
            :style="{height: simplifiedUI ? '50px' : '32px'}"
            :class="{'w-100': simplifiedUI}"
            class="transition-1s"
          >
            <span class="align-self-center">{{ $t('VÉRIFIER') }}</span>
          </ButtonBlue>
        </div>
        <BadgeNotification v-for="n in notifications" :key="n.id" :message="n.message" :fadeDelay="n.fadeDelay" :theme="n.theme"/>
      </div>
    </div>
  </div>
</template>

<script>
import ButtonBlue from '@/components/ButtonBlue.vue'
import BadgeNotification from '@/components/BadgeNotification.vue'
import businessStore from '@/store/businessStore'

export default {
  name: "MealWidget",
  components: {
    ButtonBlue,
    BadgeNotification,
  },
  data() {
    return {
      notificationsCounter: 0,
      notifications: []
    }
  },
  computed: {
    pulsate() {
      return businessStore.state.pulsateCheckAvailabilityButton
    },
    simplifiedUI() {
      return businessStore.state.simplifiedUI
    },
    availabilityLoading() {
      return businessStore.state.availabilityLoading
    },
    label() {
      return businessStore.state.meals[this.mealIndex].label
    },
    price() {
      return businessStore.state.meals[this.mealIndex].price.toFixed(2)
    },
    margin() {
      return (businessStore.state.meals[this.mealIndex].baseMargin + businessStore.state.meals[this.mealIndex].quality * businessStore.state.meals[this.mealIndex].marginQualitySensitivity).toFixed(2)
    },
    cycles() {
      return (businessStore.state.meals[this.mealIndex].baseCycles + businessStore.state.meals[this.mealIndex].quality * businessStore.state.meals[this.mealIndex].cyclesQualitySensitivity).toLocaleString().replaceAll(',', ' ')
    },
    verificationStatus() {
      return businessStore.state.meals[this.mealIndex].verificationStatus
    },
  },
  methods: {
    cleanNotificationFromId(id) {
      this.notifications.filter(n => n.id !== id)
    },
    click() {
      businessStore.commit('setPulsateCheckAvailabilityButton', false)
      businessStore.commit('checkAvailability', this.mealIndex)
    },
    watchQuality() {
      if (!this.simplifiedUI) {
        businessStore.commit('setQuality', {mealIndex: this.mealIndex, value: this.$refs.qualityInput.value})
      }
      setTimeout(this.watchQuality, 10)
    }
  },
  watch: {
    mealIndex() {
      this.$refs.qualityInput.value = businessStore.state.meals[this.mealIndex].quality
    },
  },
  mounted() {
    this.watchQuality()
  },
  props: {
    mealIndex: Number,
  }
}
</script>

<style scoped>
.pulsate {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  background: rgba(0, 90, 180, 1);
  animation: pulser 1.4s linear infinite;
  opacity: 0;
}

@keyframes pulser {
	0% {
		transform: scale(1);
		opacity: 0;
	}
  20% {
		transform: scale(1);
		opacity: 0;
	}
	60% {
		transform: scale(1.4);
		opacity: 0.4;
	}
	100% {
		transform: scale(1.50);
		opacity: 0;
	}
}
</style>