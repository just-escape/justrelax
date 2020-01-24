<template>
  <b-modal
    :id="modalId"
    body-bg-variant="dark"
    body-text-variant="light"
    @ok="ok"
  >
    <ValueModalPredefined
      v-if="inputType === 'predefined'"
      :predefinedChoices="predefinedChoices"
      :parentValue="value"
      :checked="selectedSource === 'predefined'"
      @pushValue="(newValue) => updateValueBuffer('predefined', newValue)"
    />

    <ValueModalVariable
      v-if="inputType !== 'predefined'"
      :parentValue="value"
      :inputType="inputType"
      :checked="selectedSource === 'variable'"
      @pushValue="(newValue) => updateValueBuffer('variable', newValue)"
    />

    <ValueModalFunction
      v-if="inputType !== 'predefined'"
      :modalId="modalId"
      :parentValue="value"
      :inputType="inputType"
      :checked="selectedSource === 'function'"
      @pushValue="(newValue) => updateValueBuffer('function', newValue)"
    />

    <!--<ValueModalObject
      v-if="inputType === 'object'"
      :parentValue="value"
      :checked="selectedSource === 'object'"
      @pushValue="(newValue) => updateValueBuffer('object', newValue)"
    />

    <ValueModalList
      v-if="inputType === 'list'"
      :parentValue="value"
      :checked="selectedSource === 'list'"
      @pushValue="(newValue) => updateValueBuffer('list', newValue)"
    />-->

    <ValueModalString
      v-if="inputType === 'string'"
      :parentValue="value"
      :checked="selectedSource === 'string'"
      @pushValue="(newValue) => updateValueBuffer('string', newValue)"
    />

    <ValueModalInteger
      v-if="inputType === 'integer'"
      :parentValue="value"
      :checked="selectedSource === 'integer'"
      @pushValue="(newValue) => updateValueBuffer('integer', newValue)"
    />

    <ValueModalReal
      v-if="inputType === 'real'"
      :parentValue="value"
      :checked="selectedSource === 'real'"
      @pushValue="(newValue) => updateValueBuffer('real', newValue)"
    />

    <ValueModalBoolean
      v-if="inputType === 'boolean'"
      :parentValue="value"
      :checked="selectedSource === 'boolean'"
      @pushValue="(newValue) => updateValueBuffer('boolean', newValue)"
    />
  </b-modal>
</template>

<script>
import ValueModalPredefined from '@/components/editor/ValueModalPredefined.vue'
import ValueModalVariable from '@/components/editor/ValueModalVariable.vue'
import ValueModalFunction from '@/components/editor/ValueModalFunction.vue'
// import ValueModalObject from '@/components/editor/ValueModalObject.vue'
// import ValueModalList from '@/components/editor/ValueModalList.vue'
import ValueModalString from '@/components/editor/ValueModalString.vue'
import ValueModalInteger from '@/components/editor/ValueModalInteger.vue'
import ValueModalReal from '@/components/editor/ValueModalReal.vue'
import ValueModalBoolean from '@/components/editor/ValueModalBoolean.vue'

export default {
  name: "ValueModal",
  components: {
    ValueModalPredefined,
    ValueModalVariable,
    ValueModalFunction,
    // ValueModalObject,
    // ValueModalList,
    ValueModalString,
    ValueModalInteger,
    ValueModalReal,
    ValueModalBoolean,
  },
  data() {
    return {
      valueBuffer: undefined,
      selectedSource: "string",
    }
  },
  methods: {
    ok: function() {
      this.$emit('update', this.valueBuffer)
    },
    updateValueBuffer(source, value) {
      this.selectedSource = source
      this.valueBuffer = value
    },
  },
  props: {
    modalId: String,
    value: [Object, Boolean, String, Number],
    inputType: String,
    predefinedChoices: Array,
  },
}
</script>
