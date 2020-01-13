<template>
  <b-modal
    :id="modalId"
    body-bg-variant="dark"
    body-text-variant="light"
    @ok="ok"
  >
    <select v-model="selectedContentType" class="mr-2">
      <option
        v-for="(label, value) in contentTypeOptions"
        :key="value"
        :value="value"
      >
        {{ label }}
      </option>
    </select>

    <ContextLinksModal
      :contextLinks="contextLinksBuffer"
      @updateArgument="updateArgument"
    />
  </b-modal>
</template>

<script>
import ContextLinksModal from '@/components/editor/ContextLinksModal.vue'
import rulesStore from '@/store/rulesStore.js'

export default {
  name: "ActionModal",
  components: {
    ContextLinksModal,
  },
  data() {
    return {
      selectedContentType: undefined,
      contextLinksBuffer: [],
    }
  },
  computed: {
    contentTypes() {
      return rulesStore.state.contextTypes[this.contextType]
    },
    contentTypeOptions() {
      var options = {}
      for (var i = 0 ; i < this.contentTypes.length ; i++) {
        options[this.contentTypes[i].name] = this.contentTypes[i].label
      }
      return options
    },
  },
  methods: {
    ok: function() {
      var content = {
        type: this.selectedContentType,
      }
      for (var i = 0 ; i < this.contextLinksBuffer.length ; i++) {
        if (this.contextLinksBuffer[i].type === "argument") {
          content[this.contextLinksBuffer[i].argumentId] = this.contextLinksBuffer[i].argument
        }
      }
      this.$emit('update', content)
    },
    updateArgument(argumentId, argument) {
      for (var i = 0 ; i < this.contextLinksBuffer.length ; i++) {
        if (
          this.contextLinksBuffer[i].type === "argument" &&
          this.contextLinksBuffer[i].argumentId === argumentId
        ) {
          this.contextLinksBuffer[i].argument = argument
          return
        }
      }
    },
    initArguments() {
      for (var i = 0 ; i < this.contextLinksBuffer.length ; i++) {
        if (this.contextLinksBuffer[i].type === "argument") {
          this.contextLinksBuffer[i].argument = this.content[this.contextLinksBuffer[i].argumentId]
        }
      }
    },
  },
  watch: {
    selectedContentType() {
      for (var i = 0 ; i < this.contentTypes.length ; i++) {
        if (this.contentTypes[i].name === this.selectedContentType) {
          this.contextLinksBuffer = JSON.parse(JSON.stringify(this.contentTypes[i].contextLinks))
        }
      }
    },
  },
  created() {
    this.selectedContentType = this.content.type
    this.initArguments()
  },
  props: {
    modalId: String,
    contextType: String,
    content: Object,
  }
}
</script>
