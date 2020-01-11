<template>
  <b-modal
    :id="modalId"
    @ok="ok"
  >
    <select v-model="selected" class="mr-2">
      <option disabled value="">Choose</option>
      <option v-for="(value, key) in options" :key="key" :value="key">{{ value }}</option>
    </select>
  </b-modal>
</template>

<script>
export default {
  name: "ConditionModal",
  data() {
    return {
      tmpCondition: undefined,
      options: {
        'condition 1': 'Condition 1',
        'condition 2': 'Condition 2',
        'condition 3': 'Condition 3',
        'condition 4': 'Condition 4',
      },
    }
  },
  computed: {
    selected: {
      get() {
        return this.tmpCondition.name
      },
      set(value) {
        this.tmpCondition.name = value
      }
    }
  },
  methods: {
    ok: function() {
      // Copy to avoid sending all vue getters/setters
      let condition = { ...this.tmpCondition }
      this.$emit('update', condition)
    }
  },
  created() {
    this.tmpCondition = { ...this.condition }
  },
  props: {
    modalId: String,
    condition: Object,
  }
}
</script>
