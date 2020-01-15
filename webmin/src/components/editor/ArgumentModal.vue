<template>
  <b-modal
    :id="modalId"
    body-bg-variant="dark"
    body-text-variant="light"
    @ok="ok"
  >
    <ArgumentModalVariable
      :parentArgument="argument"
      :checked="selectedSource === 'variable'"
      @pushValue="(value) => updateArgumentBuffer('variable', value)"
    />

    <ArgumentModalFunction
      :modalId="modalId"
      :parentArgument="argument"
      :checked="selectedSource === 'function'"
      @pushValue="(value) => updateArgumentBuffer('function', value)"
    />

    <ArgumentModalObject
      :parentArgument="argument"
      :checked="selectedSource === 'object'"
      @pushValue="(value) => updateArgumentBuffer('object', value)"
    />

    <ArgumentModalList
      :parentArgument="argument"
      :checked="selectedSource === 'list'"
      @pushValue="(value) => updateArgumentBuffer('list', value)"
    />

    <ArgumentModalString
      :parentArgument="argument"
      :checked="selectedSource === 'string'"
      @pushValue="(value) => updateArgumentBuffer('string', value)"
    />

    <ArgumentModalInteger
      :parentArgument="argument"
      :checked="selectedSource === 'integer'"
      @pushValue="(value) => updateArgumentBuffer('integer', value)"
    />

    <ArgumentModalReal
      :parentArgument="argument"
      :checked="selectedSource === 'real'"
      @pushValue="(value) => updateArgumentBuffer('real', value)"
    />

    <ArgumentModalSpecial
      :parentArgument="argument"
      :checked="selectedSource === 'special'"
      @pushValue="(value) => updateArgumentBuffer('special', value)"
    />
  </b-modal>
</template>

<script>
import ArgumentModalVariable from '@/components/editor/ArgumentModalVariable.vue'
import ArgumentModalFunction from '@/components/editor/ArgumentModalFunction.vue'
import ArgumentModalObject from '@/components/editor/ArgumentModalObject.vue'
import ArgumentModalList from '@/components/editor/ArgumentModalList.vue'
import ArgumentModalString from '@/components/editor/ArgumentModalString.vue'
import ArgumentModalInteger from '@/components/editor/ArgumentModalInteger.vue'
import ArgumentModalReal from '@/components/editor/ArgumentModalReal.vue'
import ArgumentModalSpecial from '@/components/editor/ArgumentModalSpecial.vue'

export default {
  name: "ArgumentModal",
  components: {
    ArgumentModalVariable,
    ArgumentModalFunction,
    ArgumentModalObject,
    ArgumentModalList,
    ArgumentModalString,
    ArgumentModalInteger,
    ArgumentModalReal,
    ArgumentModalSpecial,
  },
  data() {
    return {
      argumentBuffer: undefined,
      selectedSource: "string",
    }
  },
  methods: {
    ok: function() {
      this.$emit('updateArgument', this.argumentBuffer)
    },
    updateArgumentBuffer(source, value) {
      this.selectedSource = source
      this.argumentBuffer = value
    },
  },
  props: {
    modalId: String,
    argument: [Object, Boolean, String, Number],
  },
}
</script>
