<template>
  <div class="d-flex flex-row">
    <div class="mr-3">
      <PulsatingPrimaryButton @click="attemptOrder" size="lg" :pulse="pulse" :disabled="isCartEmpty">
        Passer commande
      </PulsatingPrimaryButton>
    </div>
    <div>
      <b-form-radio-group
        id="radio"
        v-model="selected"
        :options="options"
        stacked
      >
      </b-form-radio-group>
    </div>
  </div>
</template>

<script>
import PulsatingPrimaryButton from "@/components/PulsatingPrimaryButton.vue"
import orderStore from "@/store/orderStore.js"

export default {
  name: "RightPanelButtons",
  components: {
    PulsatingPrimaryButton,
  },
  data() {
    return {
      pulse: false,
      selected: "first",
      options: [
        {text: "À emporter", value: "first"},
        {text: "Sur place", value: "second"},
      ]
    }
  },
  computed: {
    isCartEmpty: function() {
      return orderStore.getters.isCartEmpty
    },
  },
  methods: {
    startPulse: function() {
      if (!this.isCartEmpty) {
        this.pulse = true
      }
    },
    attemptOrder: function() {
      orderStore.commit('attemptOrder')
    },
  },
  watch: {
    isCartEmpty: function(newValue) {
      if (newValue) {
        this.pulse = false
      } else {
        setTimeout(this.startPulse, 10000)
      }
    }
  }
}
</script>
