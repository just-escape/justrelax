<template>
  <div class="glowing-container w-100 mb-4 p-3">
    <div class="d-flex flex-row justify-content-center mb-4" style="font-size: 20px">{{label}}</div>
    <div class="d-flex flex-row justify-content-between mb-2">
      <div style="font-style: italic">Prix</div>
      <div>{{price}} NéoFrancs</div>
    </div>
    <div class="d-flex flex-row justify-content-between mb-2">
      <div style="font-style: italic">Marge financière</div>
      <div>{{margin}} NéoFrancs</div>
    </div>
    <div class="d-flex flex-row justify-content-between mb-2">
      <div style="font-style: italic">Temps de production</div>
      <div>{{cycles}} cycles</div>
    </div>
    <div class="d-flex flex-row justify-content-between mb-2">
      <div style="font-style: italic">Qualité de production</div>
      <div><input ref="qualityInput" type="range" min="0" max="100"></div>
    </div>
    <div class="d-flex flex-row justify-content-between align-items-center mb-2">
      <div style="font-style: italic">Disponibilité ingrédients</div>
      <div class="position-relative">
        <div style="width: 100px; height: 30px" class="d-flex align-items-center justify-content-center">
          <div v-if="availabilityLoading" class="loading"></div>
          <ButtonBlue v-else @click="click">
            <span class="align-self-center">VÉRIFIER</span>
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
      businessStore.commit('checkAvailability', this.mealIndex)
    },
    watchQuality() {
      businessStore.commit('setQuality', {mealIndex: this.mealIndex, value: this.$refs.qualityInput.value})
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
