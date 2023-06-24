import fetch from '@/utils/fetch'
/**
 * 
 * @param {startTimestamp,endTimestamp,pageIndex,pageSize} query 
 * @returns 
 */
export function getLastData() {
    return fetch({
        url: '/api/getLast',
        method: 'get',
    })
}

export function setFanInfo(query) {
    return fetch({
        url: '/api/setFan',
        method: 'post',
        params: query
    })
}

/**
 * 
 * @param {startTimestamp,endTimestamp,pageIndex,pageSize} query 
 * @returns 
 */
export function getFanInfo(query) {
    return fetch({
        url: '/api/getFan',
        method: 'get',
        params: query
    })
}