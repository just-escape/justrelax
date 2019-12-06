<template>
  <div class="d-flex flex-row">
    <div class="mr-3">
      <b-btn variant="primary" size="lg">
        Passer commande
      </b-btn>
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
export default {
  name: "RightPanelButtons",
  data() {
    return {
      selected: "first",
      options: [
        {text: "À emporter", value: "first"},
        {text: "Sur place", value: "second"},
      ]
    }
  }
}
</script>