<template>
  <div class="glowing-container h-100 w-100 mb-4 p-3">
    <div class="d-flex flex-row justify-content-center mb-3" style="font-size: 20px">{{label}}</div>
    <div class="d-flex flex-row justify-content-between mb-1">
      <div style="font-style: italic">Prix</div>
      <div>{{price}} NéoFrancs</div>
    </div>
    <div class="d-flex flex-row justify-content-between mb-1">
      <div style="font-style: italic">Marge financière</div>
      <div>{{margin}} NéoFrancs</div>
    </div>
    <div class="d-flex flex-row justify-content-between mb-1">
      <div style="font-style: italic">Temps de production</div>
      <div>{{cycles}} cycles</div>
    </div>
    <div class="d-flex flex-row justify-content-between mb-1">
      <div style="font-style: italic">Qualité de production</div>
      <div><input ref="qualityInput" type="range" min="0" max="100"></div>
    </div>
    <div class="d-flex flex-row justify-content-between align-items-center">
      <div style="font-style: italic">Disponibilité ingrédients</div>
      <div class="position-relative">
        <div style="width: 100px; height: 30px" class="d-flex align-items-center justify-content-center">
          <div v-if="loading" class="loading"></div>
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
      loading: false,
      notificationsCounter: 0,
      notifications: []
    }
  },
  computed: {
    availabilityNotificationSignal() {
      return businessStore.state.availabilityNotificationSignal
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
      this.loading = true 
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
    availabilityNotificationSignal() {
      this.loading = false

      /*for (let meal of businessStore.state.meals) {
        if (meal.id === businessStore.state.availabilityNotificationId) {
          let thisId = this.notificationsCounter++
          let message = businessStore.state.availabilityNotificationMissingIngredients ? "Au moins une capsule pour<br/>" : "Toutes les capsules pour<br/>"
          message += "produire des " + meal.labelPlural + "<br/>"
          message += businessStore.state.availabilityNotificationMissingIngredients ? "n'est pas engagée" : "sont engagées"
          let theme = businessStore.state.availabilityNotificationMissingIngredients ? 'danger' : 'blue'
          this.notifications.push({id: thisId, message: message, fadeDelay: 3000, theme: theme})
          setTimeout(this.cleanNotificationFromId, 3100, thisId)
        }
      }*/
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
.loading {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 4px solid rgba(0, 209, 182, .3);
  border-radius: 50%;
  border-top-color: #00d1b6;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { -webkit-transform: rotate(360deg); }
}
@-webkit-keyframes spin {
  to { -webkit-transform: rotate(360deg); }
}
</style>