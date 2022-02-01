<template>
    <div class="text-jaffa">
        {{ face }}
    </div>
</template>

<script>
export default {
  name: "MiniSokobanLevel",
  components: {
  },
  props: ['sceneSize', 'transform', 'face'],
}
</script>