<template>
  <a :href="url">
    <div class="p-3">
      <i :class="icon + ' fa-fw fa-lg mr-3'"></i>{{ label }}
    </div>
  </a>
</template>

<script>
export default {
  name: 'AppNavTab',
  props: ['url', 'icon', 'label']
}
</script>
