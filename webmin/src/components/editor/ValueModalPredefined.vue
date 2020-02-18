<template>
  <div class="row mb-3">
    <div @click="pushMyValue" class="d-flex align-items-center col-3">
      <input type="radio" :checked="checked">
      <span class="ml-2">{{ $t('editor.predefined') }}</span>
    </div>
    <div class="col-9">
      <select v-model="selectedChoice" @focus="pushMyValue">
        <option
          v-for="value in predefinedChoices"
          :key="value"
          :value="value"
        >
          {{ $t('editor.templates.' + templateName + '.' + value) }}
        </option>
      </select>
    </div>
  </div>
</template>

<script>
import valueModalMixin from '@/components/editor/valueModalMixin.js'

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
  },
  created() {
    if (this.predefinedChoices.includes(this.parentValue)) {
      this.valueBuffer = this.parentValue
      this.pushMyValue()
    } else {
      this.valueBuffer = this.predefinedChoices[0]
    }
  },
  props: {
    predefinedChoices: Array,
    templateName: String,
  }
}
</script>
