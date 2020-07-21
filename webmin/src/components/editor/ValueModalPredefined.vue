<template>
  <div class="row mb-3">
    <div @click="pushMyValue" class="d-flex align-items-center col-3">
      <input type="radio" :checked="checked">
      <span class="ml-2">{{ $t('editor.predefined') }}</span>
    </div>
    <div class="col-9">
      <select v-model="selectedChoice" @focus="pushMyValue">
        <option
          v-for="(value, valueIndex) in predefinedChoices"
          :key="valueIndex"
          :value="value"
        >
          {{ getChoice(value) }}
        </option>
      </select>
    </div>
  </div>
</template>

<script>
import valueModalMixin from '@/components/editor/valueModalMixin.js'
import editorStore from '@/store/editorStore.js'

export default {
  name: "ValueModalPredefined",
  mixins: [valueModalMixin],
  computed: {
    selectedChoice: {
      get() {
        return this.valueBuffer
      },
      set(value) {
        this.valueBuffer = value
        this.pushMyValue()
      },
    },
    getChoice() {
      return function(value) {
        if (value.rule !== undefined) {
          let rules = editorStore.state.rules
          for (var rule of rules) {
            if (rule.id === value.rule) {
              return rule.name
            }
          }
          // Data is corrupted or the rule must have been deleted
          return this.$t('editor.no_rule')
        } else {
          return this.$t('editor.templates.' + this.templateName + '.' + value)
        }
      }
    },
  },
  created() {
    for (let pc of this.predefinedChoices) {
      if (JSON.stringify(pc) == JSON.stringify(this.parentValue)) {
        this.valueBuffer = JSON.parse(JSON.stringify(this.parentValue))
        this.pushMyValue()
        return
      }
    }
    this.valueBuffer = this.predefinedChoices[0]
  },
  props: {
    predefinedChoices: Array,
    templateName: String,
  },
}
</script>
