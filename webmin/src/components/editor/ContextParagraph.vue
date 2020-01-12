<template>
  <div>
    <div class="text-jaffa">
      <i class="fas fa-fw" :class="icon"></i> {{ title }}
    </div>
    <div class="container-fluid">
      <div class="row">
        <div class="col">
          <div class="d-flex flex-column">
            <ContextLine
              v-for="l in lines"
              :key="l.index"
              :content="l"
              :contextType="contextType"
              @updateContent="updateContent"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ContextLine from "@/components/editor/ContextLine.vue"

export default {
  name: 'ContextParagraph',
  components: {
    ContextLine
  },
  computed: {
    icon() {
      if (this.contextType === 'trigger') {
        return ['fa-play']
      } else if (this.contextType === 'condition') {
        return ['fa-question']
      } else if (this.contextType === 'action') {
        return ['fa-exclamation']
      } else {
        return []
      }
    }
  },
  methods: {
    updateContent(content) {
      this.$emit('updateLine', content)
    }
  },
  props: {
    title: String,
    contextType: String,
    lines: Array,
  }
}
</script>
